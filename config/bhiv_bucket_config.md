# BHIV Bucket Configuration

## Environment Variables Needed

When you get Nipun's BHIV bucket credentials, add these to your `.env` file:

```bash
# BHIV Bucket Configuration
BHIV_BUCKET_ENABLED=true
BHIV_BUCKET_NAME=your-actual-bucket-name
BHIV_ACCESS_KEY=your-actual-access-key
BHIV_SECRET_KEY=your-actual-secret-key
BHIV_ENDPOINT=https://your-actual-s3-endpoint.com
BHIV_REGION=us-east-1
```

## Current Status

- ✅ **Preview Manager**: Implemented with AWS S3 SDK
- ✅ **Signed URLs**: 24-hour expiration with verification
- ✅ **Local Fallback**: Works without bucket credentials
- ✅ **Three.js Integration**: GLB format support
- ⏳ **Waiting for**: Nipun's actual bucket credentials

## Features Ready

1. **Signed URL Generation**: `generate_preview(spec_data)`
2. **URL Verification**: `verify_preview_url(spec_id, expires, signature)`
3. **Preview Refresh**: `refresh_preview(spec_id, spec_data)` after `/switch`
4. **Cleanup**: `cleanup_stale_previews()` for maintenance
5. **Three.js Data**: `get_threejs_data(spec_data)` for frontend
6. **HTML Viewer**: `generate_viewer_html(spec_data)` for testing

## Testing

Current implementation uses local storage fallback:
- Preview files stored in `preview_storage/`
- Signed URLs: `/api/v1/preview/local/{spec_id}?expires={timestamp}&signature={hash}`
- Cache file: `preview_storage/preview_cache.json`

## Production Switch

Once you provide real credentials:
1. Update `.env` with actual values
2. Set `BHIV_BUCKET_ENABLED=true`
3. System automatically switches to bucket storage
4. All existing endpoints continue working seamlessly