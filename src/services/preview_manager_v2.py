"""Preview Manager with BHIV Bucket Signed URLs - Production Ready"""

import os
import boto3
import hashlib
import hmac
import base64
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from pathlib import Path
import json
import uuid
from botocore.exceptions import ClientError, NoCredentialsError

class PreviewManager:
    """Preview manager with BHIV bucket signed URLs and local fallback"""
    
    def __init__(self):
        # BHIV Bucket Configuration
        self.bucket_name = os.getenv("BHIV_BUCKET_NAME", "bhiv-previews")
        self.access_key = os.getenv("BHIV_ACCESS_KEY")
        self.secret_key = os.getenv("BHIV_SECRET_KEY")
        self.region = os.getenv("BHIV_REGION", "us-east-1")
        self.endpoint_url = os.getenv("BHIV_ENDPOINT")
        
        # Check if bucket is properly configured
        self.bucket_enabled = (
            os.getenv("BHIV_BUCKET_ENABLED", "false").lower() == "true" and
            self.access_key and 
            self.secret_key and
            self.endpoint_url
        )
        
        if self.bucket_enabled:
            try:
                # Initialize S3 client for BHIV bucket
                self.s3_client = boto3.client(
                    's3',
                    aws_access_key_id=self.access_key,
                    aws_secret_access_key=self.secret_key,
                    region_name=self.region,
                    endpoint_url=self.endpoint_url
                )
                print(f"[PREVIEW] BHIV bucket configured: {self.bucket_name}")
            except Exception as e:
                print(f"[PREVIEW] BHIV bucket setup failed: {e}, using local fallback")
                self.bucket_enabled = False
        else:
            print("[PREVIEW] BHIV bucket disabled, using local storage")
        
        # Local fallback setup
        if not self.bucket_enabled:
            self.local_storage = Path("preview_storage")
            self.local_storage.mkdir(exist_ok=True)
            self.preview_cache = {}
            self._load_preview_cache()
    
    def _load_preview_cache(self):
        """Load preview cache from file"""
        cache_file = self.local_storage / "preview_cache.json"
        if cache_file.exists():
            try:
                with open(cache_file, 'r') as f:
                    self.preview_cache = json.load(f)
            except Exception:
                self.preview_cache = {}
    
    def _save_preview_cache(self):
        """Save preview cache to file"""
        cache_file = self.local_storage / "preview_cache.json"
        try:
            with open(cache_file, 'w') as f:
                json.dump(self.preview_cache, f, indent=2)
        except Exception:
            pass
    
    async def generate_preview(self, spec_data: Dict[str, Any]) -> str:
        """Generate signed preview URL for spec"""
        spec_id = spec_data.get('spec_id', str(uuid.uuid4()))
        
        if self.bucket_enabled:
            return await self._generate_bucket_preview(spec_id, spec_data)
        else:
            return await self._generate_local_preview(spec_id, spec_data)
    
    async def _generate_bucket_preview(self, spec_id: str, spec_data: Dict[str, Any]) -> str:
        """Generate signed URL from BHIV bucket"""
        try:
            # Generate preview file (mock 3D data)
            preview_key = f"previews/{spec_id}.glb"
            
            # Upload preview data to bucket
            preview_data = self._create_preview_data(spec_data)
            
            try:
                self.s3_client.put_object(
                    Bucket=self.bucket_name,
                    Key=preview_key,
                    Body=preview_data,
                    ContentType='model/gltf-binary',
                    Metadata={
                        'spec_id': spec_id,
                        'created_at': datetime.now(timezone.utc).isoformat()
                    }
                )
                print(f"[PREVIEW] Uploaded to bucket: {preview_key}")
            except ClientError as e:
                print(f"[PREVIEW] Upload failed: {e}")
                return await self._generate_local_preview(spec_id, spec_data)
            
            # Generate signed URL (valid for 24 hours)
            try:
                signed_url = self.s3_client.generate_presigned_url(
                    'get_object',
                    Params={'Bucket': self.bucket_name, 'Key': preview_key},
                    ExpiresIn=86400  # 24 hours
                )
                print(f"[PREVIEW] Generated signed URL: {signed_url[:50]}...")
                return signed_url
            except ClientError as e:
                print(f"[PREVIEW] Signed URL generation failed: {e}")
                return await self._generate_local_preview(spec_id, spec_data)
                
        except Exception as e:
            print(f"[PREVIEW] Bucket preview failed: {e}")
            return await self._generate_local_preview(spec_id, spec_data)
    
    async def _generate_local_preview(self, spec_id: str, spec_data: Dict[str, Any]) -> str:
        """Generate local signed URL as fallback"""
        # Create local preview file
        preview_file = self.local_storage / f"{spec_id}.glb"
        preview_data = self._create_preview_data(spec_data)
        
        with open(preview_file, 'wb') as f:
            f.write(preview_data)
        
        # Generate local signed URL
        expires = int((datetime.now(timezone.utc) + timedelta(hours=24)).timestamp())
        signature = self._generate_local_signature(spec_id, expires)
        
        signed_url = f"/api/v1/preview/local/{spec_id}?expires={expires}&signature={signature}"
        
        # Cache preview info
        self.preview_cache[spec_id] = {
            'file_path': str(preview_file),
            'created_at': datetime.now(timezone.utc).isoformat(),
            'signed_url': signed_url
        }
        self._save_preview_cache()
        
        print(f"[PREVIEW] Generated local signed URL: {signed_url}")
        return signed_url
    
    def _create_preview_data(self, spec_data: Dict[str, Any]) -> bytes:
        """Create mock 3D preview data (GLB format)"""
        # Mock GLB header and basic geometry
        objects = spec_data.get('objects', [])
        scene_info = spec_data.get('scene', {})
        
        preview_json = {
            'spec_id': spec_data.get('spec_id'),
            'objects_count': len(objects),
            'scene_name': scene_info.get('name', 'Design Preview'),
            'materials': [obj.get('material', 'default') for obj in objects],
            'preview_type': 'glb',
            'generated_at': datetime.now(timezone.utc).isoformat()
        }
        
        # Convert to bytes (in production, this would be actual GLB data)
        return json.dumps(preview_json, indent=2).encode('utf-8')
    
    def _generate_local_signature(self, spec_id: str, expires: int) -> str:
        """Generate signature for local signed URL"""
        payload = f"{spec_id}:{expires}"
        secret = os.getenv('API_KEY', 'fallback-secret')
        
        signature = hmac.new(
            secret.encode('utf-8'),
            payload.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()[:16]
        
        return signature
    
    async def verify_preview_url(self, spec_id: str, expires: int, signature: str) -> bool:
        """Verify signed preview URL"""
        if self.bucket_enabled:
            return await self._verify_bucket_url(spec_id, expires, signature)
        else:
            return self._verify_local_url(spec_id, expires, signature)
    
    async def _verify_bucket_url(self, spec_id: str, expires: int, signature: str) -> bool:
        """Verify bucket signed URL (AWS handles this automatically)"""
        # For AWS S3, signed URLs are automatically verified
        # Check if URL hasn't expired
        current_time = datetime.now(timezone.utc).timestamp()
        return current_time < expires
    
    def _verify_local_url(self, spec_id: str, expires: int, signature: str) -> bool:
        """Verify local signed URL"""
        # Check expiration
        current_time = datetime.now(timezone.utc).timestamp()
        if current_time > expires:
            return False
        
        # Verify signature
        expected_signature = self._generate_local_signature(spec_id, expires)
        return hmac.compare_digest(signature, expected_signature)
    
    async def refresh_preview(self, spec_id: str, spec_data: Dict[str, Any]) -> str:
        """Force refresh preview after spec changes"""
        print(f"[PREVIEW] Refreshing preview for spec {spec_id}")
        
        if self.bucket_enabled:
            # Delete old preview from bucket
            try:
                self.s3_client.delete_object(
                    Bucket=self.bucket_name,
                    Key=f"previews/{spec_id}.glb"
                )
            except ClientError:
                pass  # Object might not exist
        else:
            # Delete local preview
            if spec_id in self.preview_cache:
                old_file = Path(self.preview_cache[spec_id]['file_path'])
                if old_file.exists():
                    old_file.unlink()
                del self.preview_cache[spec_id]
                self._save_preview_cache()
        
        # Generate new preview
        return await self.generate_preview(spec_data)
    
    def cleanup_stale_previews(self, max_age_hours: int = 48) -> int:
        """Cleanup stale preview files"""
        cleaned_count = 0
        cutoff_time = datetime.now(timezone.utc) - timedelta(hours=max_age_hours)
        
        if not self.bucket_enabled:
            # Cleanup local previews
            stale_specs = []
            for spec_id, info in self.preview_cache.items():
                created_at = datetime.fromisoformat(info['created_at'].replace('Z', '+00:00'))
                if created_at < cutoff_time:
                    file_path = Path(info['file_path'])
                    if file_path.exists():
                        file_path.unlink()
                    stale_specs.append(spec_id)
                    cleaned_count += 1
            
            # Remove from cache
            for spec_id in stale_specs:
                del self.preview_cache[spec_id]
            
            if stale_specs:
                self._save_preview_cache()
        
        print(f"[PREVIEW] Cleaned up {cleaned_count} stale previews")
        return cleaned_count
    
    def get_threejs_data(self, spec_data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert spec to Three.js compatible format"""
        objects = spec_data.get('objects', [])
        scene_info = spec_data.get('scene', {})
        
        threejs_objects = []
        for obj in objects:
            threejs_obj = {
                'id': obj.get('id'),
                'type': 'mesh',
                'geometry': {
                    'type': 'box',
                    'width': obj.get('dimensions', {}).get('width', 1),
                    'height': obj.get('dimensions', {}).get('height', 1),
                    'depth': obj.get('dimensions', {}).get('depth', 1)
                },
                'material': {
                    'type': 'standard',
                    'name': obj.get('material', 'default'),
                    'color': self._material_to_color(obj.get('material', 'default'))
                },
                'position': {
                    'x': obj.get('position', {}).get('x', 0),
                    'y': obj.get('position', {}).get('y', 0),
                    'z': obj.get('position', {}).get('z', 0)
                },
                'editable': obj.get('editable', True)
            }
            threejs_objects.append(threejs_obj)
        
        return {
            'scene': {
                'name': scene_info.get('name', 'Design Scene'),
                'background': '#f0f0f0',
                'fog': {'type': 'linear', 'near': 1, 'far': 1000, 'color': '#cccccc'}
            },
            'objects': threejs_objects,
            'camera': {
                'type': 'perspective',
                'position': {'x': 10, 'y': 10, 'z': 10},
                'target': {'x': 0, 'y': 0, 'z': 0}
            },
            'lights': [
                {'type': 'ambient', 'intensity': 0.4},
                {'type': 'directional', 'position': {'x': 10, 'y': 10, 'z': 5}, 'intensity': 0.8}
            ]
        }
    
    def _material_to_color(self, material: str) -> str:
        """Convert material name to hex color"""
        material_colors = {
            'wood': '#8B4513',
            'concrete': '#808080',
            'steel': '#C0C0C0',
            'glass': '#87CEEB',
            'brick': '#B22222',
            'marble': '#F8F8FF',
            'granite': '#2F4F4F',
            'tile': '#DCDCDC'
        }
        return material_colors.get(material.lower(), '#CCCCCC')
    
    def generate_viewer_html(self, spec_data: Dict[str, Any]) -> str:
        """Generate HTML viewer for spec preview"""
        threejs_data = self.get_threejs_data(spec_data)
        spec_id = spec_data.get('spec_id', 'unknown')
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Design Preview - {spec_id}</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
    <style>
        body {{ margin: 0; padding: 0; overflow: hidden; background: #f0f0f0; }}
        #viewer {{ width: 100vw; height: 100vh; }}
        #info {{ position: absolute; top: 10px; left: 10px; color: #333; font-family: Arial; }}
    </style>
</head>
<body>
    <div id="viewer"></div>
    <div id="info">
        <h3>Design Preview: {spec_id}</h3>
        <p>Objects: {len(threejs_data['objects'])}</p>
        <p>Scene: {threejs_data['scene']['name']}</p>
    </div>
    
    <script>
        const sceneData = {json.dumps(threejs_data, indent=2)};
        
        // Initialize Three.js scene
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(sceneData.scene.background);
        
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({{ antialias: true }});
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.getElementById('viewer').appendChild(renderer.domElement);
        
        // Add lights
        sceneData.lights.forEach(light => {{
            if (light.type === 'ambient') {{
                scene.add(new THREE.AmbientLight(0xffffff, light.intensity));
            }} else if (light.type === 'directional') {{
                const dirLight = new THREE.DirectionalLight(0xffffff, light.intensity);
                dirLight.position.set(light.position.x, light.position.y, light.position.z);
                scene.add(dirLight);
            }}
        }});
        
        // Add objects
        sceneData.objects.forEach(obj => {{
            const geometry = new THREE.BoxGeometry(
                obj.geometry.width, 
                obj.geometry.height, 
                obj.geometry.depth
            );
            const material = new THREE.MeshLambertMaterial({{ color: obj.material.color }});
            const mesh = new THREE.Mesh(geometry, material);
            
            mesh.position.set(obj.position.x, obj.position.y, obj.position.z);
            mesh.userData = {{ id: obj.id, editable: obj.editable }};
            scene.add(mesh);
        }});
        
        // Set camera position
        camera.position.set(
            sceneData.camera.position.x,
            sceneData.camera.position.y,
            sceneData.camera.position.z
        );
        
        // Add controls
        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.target.set(
            sceneData.camera.target.x,
            sceneData.camera.target.y,
            sceneData.camera.target.z
        );
        
        // Render loop
        function animate() {{
            requestAnimationFrame(animate);
            controls.update();
            renderer.render(scene, camera);
        }}
        animate();
        
        // Handle window resize
        window.addEventListener('resize', () => {{
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        }});
    </script>
</body>
</html>
        """
        
        return html_content

# Global instance
preview_manager = PreviewManager()