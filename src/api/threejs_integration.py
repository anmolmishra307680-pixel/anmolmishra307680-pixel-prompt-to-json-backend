"""Three.js Frontend Integration - Transform specs to Three.js format"""

from typing import Dict, Any, List
from datetime import datetime

def transform_to_three_js(spec_data: Dict[str, Any]) -> Dict[str, Any]:
    """Transform spec data to Three.js compatible format"""
    objects = spec_data.get('objects', [])
    scene_info = spec_data.get('scene', {})
    
    # Transform objects to Three.js meshes
    three_js_objects = []
    for obj in objects:
        three_js_obj = {
            "id": obj.get('id'),
            "type": "mesh",
            "geometry": {
                "type": "box",
                "width": obj.get('dimensions', {}).get('width', 1),
                "height": obj.get('dimensions', {}).get('height', 1),
                "depth": obj.get('dimensions', {}).get('depth', 1)
            },
            "material": {
                "type": "standard",
                "name": obj.get('material', 'default'),
                "color": _material_to_color(obj.get('material', 'default')),
                "roughness": 0.5,
                "metalness": 0.1
            },
            "position": {
                "x": obj.get('position', {}).get('x', 0),
                "y": obj.get('position', {}).get('y', 0),
                "z": obj.get('position', {}).get('z', 0)
            },
            "rotation": {"x": 0, "y": 0, "z": 0},
            "scale": {"x": 1, "y": 1, "z": 1},
            "editable": obj.get('editable', True),
            "userData": {
                "object_type": obj.get('type'),
                "properties": obj.get('properties', {})
            }
        }
        three_js_objects.append(three_js_obj)
    
    # Scene configuration
    scene_config = {
        "name": scene_info.get('name', 'Design Scene'),
        "background": "#f5f5f5",
        "fog": {
            "type": "linear",
            "near": 1,
            "far": 1000,
            "color": "#cccccc"
        },
        "environment": "studio"
    }
    
    # Camera setup
    camera_config = {
        "type": "perspective",
        "fov": 75,
        "aspect": 16/9,
        "near": 0.1,
        "far": 1000,
        "position": {"x": 10, "y": 10, "z": 10},
        "target": {"x": 0, "y": 0, "z": 0}
    }
    
    # Lighting setup
    lights = [
        {
            "type": "ambient",
            "color": "#ffffff",
            "intensity": 0.4
        },
        {
            "type": "directional",
            "color": "#ffffff",
            "intensity": 0.8,
            "position": {"x": 10, "y": 10, "z": 5},
            "castShadow": True
        },
        {
            "type": "point",
            "color": "#ffffff",
            "intensity": 0.3,
            "position": {"x": -10, "y": 5, "z": -5}
        }
    ]
    
    # Controls configuration
    controls = {
        "type": "orbit",
        "enableDamping": True,
        "dampingFactor": 0.05,
        "enableZoom": True,
        "enablePan": True,
        "enableRotate": True,
        "autoRotate": False,
        "maxPolarAngle": 1.5708  # 90 degrees
    }
    
    return {
        "scene": scene_config,
        "objects": three_js_objects,
        "camera": camera_config,
        "lights": lights,
        "controls": controls,
        "metadata": {
            "spec_id": spec_data.get('spec_id'),
            "total_objects": len(three_js_objects),
            "generated_at": datetime.now().isoformat(),
            "version": "1.0"
        }
    }

def _material_to_color(material: str) -> str:
    """Convert material name to hex color for Three.js"""
    material_colors = {
        'wood': '#8B4513',
        'concrete': '#808080', 
        'steel': '#C0C0C0',
        'glass': '#87CEEB',
        'brick': '#B22222',
        'marble': '#F8F8FF',
        'granite': '#2F4F4F',
        'tile': '#DCDCDC',
        'aluminum': '#A8A8A8',
        'copper': '#B87333',
        'plastic': '#FFE4B5',
        'fabric': '#DDA0DD',
        'leather': '#8B4513',
        'ceramic': '#F5F5DC'
    }
    return material_colors.get(material.lower(), '#CCCCCC')

def generate_react_three_fiber_code(spec_id: str, three_js_data: Dict[str, Any]) -> str:
    """Generate React Three Fiber component code"""
    objects_jsx = []
    
    for obj in three_js_data['objects']:
        obj_jsx = f"""
        <mesh
          key="{obj['id']}"
          position={[obj['position']['x'], obj['position']['y'], obj['position']['z']]}
          userData={{{{ id: '{obj['id']}', editable: {str(obj['editable']).lower()} }}}}
        >
          <boxGeometry args={[{obj['geometry']['width']}, {obj['geometry']['height']}, {obj['geometry']['depth']}]} />
          <meshStandardMaterial 
            color="{obj['material']['color']}"
            roughness={obj['material']['roughness']}
            metalness={obj['material']['metalness']}
          />
        </mesh>"""
        objects_jsx.append(obj_jsx)
    
    component_code = f"""
import React from 'react';
import {{ Canvas }} from '@react-three/fiber';
import {{ OrbitControls, Environment }} from '@react-three/drei';

export default function DesignViewer_{spec_id.replace('-', '_')}() {{
  return (
    <Canvas
      camera={{{{
        position: [{three_js_data['camera']['position']['x']}, {three_js_data['camera']['position']['y']}, {three_js_data['camera']['position']['z']}],
        fov: {three_js_data['camera']['fov']}
      }}}}
      style={{{{ height: '100vh', background: '{three_js_data['scene']['background']}' }}}}
    >
      <ambientLight intensity={three_js_data['lights'][0]['intensity']} />
      <directionalLight 
        position={[{three_js_data['lights'][1]['position']['x']}, {three_js_data['lights'][1]['position']['y']}, {three_js_data['lights'][1]['position']['z']}]}
        intensity={three_js_data['lights'][1]['intensity']}
        castShadow
      />
      
      {chr(10).join(objects_jsx)}
      
      <OrbitControls
        enableDamping={{{str(three_js_data['controls']['enableDamping']).lower()}}}
        dampingFactor={{{three_js_data['controls']['dampingFactor']}}}
        enableZoom={{{str(three_js_data['controls']['enableZoom']).lower()}}}
        enablePan={{{str(three_js_data['controls']['enablePan']).lower()}}}
        maxPolarAngle={{{three_js_data['controls']['maxPolarAngle']}}}
      />
      
      <Environment preset="studio" />
    </Canvas>
  );
}}
"""
    
    return component_code