# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import uuid
from typing import Any
from google import genai
from google.adk.tools.tool_context import ToolContext
from google.cloud import storage
from google.genai import types

PROJECT_ID = "qwiklabs-gcp-04-f5e809382e15"
BUCKET_NAME = "stock-price-tracer-assets-qwiklabs-gcp-04-f5e809382e15"


async def generate_stock_image(
    prompt: str,
    tool_context: ToolContext,
) -> dict[str, Any] | str:
    """Generates a financial visual, chart graphic, or stock brand badge using the gemini-3.1-flash-lite-image model in global region.
    Saves the image to the Playground Artifacts panel and uploads it directly to the public Cloud Storage bucket.

    Args:
        prompt: Description of the stock illustration, financial chart, or badge to generate.
        tool_context: ADK ToolContext to save the artifact in the session.

    Returns:
        A dictionary containing the public HTTPS URL, artifact filename, and status.
    """
    try:
        # 1. Initialize Vertex AI GenAI Client in global region
        client = genai.Client(
            vertexai=True,
            project=PROJECT_ID,
            location="global",
        )

        # 2. Generate image using gemini-3.1-flash-lite-image
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite-image",
            contents=prompt,
            config=types.GenerateContentConfig(response_modalities=["IMAGE"]),
        )

        image_bytes = None
        mime_type = "image/jpeg"
        if response.candidates and response.candidates[0].content:
            for part in response.candidates[0].content.parts:
                if part.inline_data and part.inline_data.data:
                    image_bytes = part.inline_data.data
                    mime_type = part.inline_data.mime_type or "image/jpeg"
                    break

        if not image_bytes:
            return "Failed to generate image: no image data returned by model."

        # 3. Create unique filename
        ext = "jpg" if "jpeg" in mime_type else ("png" if "png" in mime_type else "img")
        filename = f"stock_chart_{uuid.uuid4().hex[:8]}.{ext}"

        # 4. Save artifact with tool_context for the Playground Artifacts panel
        if tool_context:
            artifact_part = types.Part.from_bytes(data=image_bytes, mime_type=mime_type)
            await tool_context.save_artifact(filename=filename, artifact=artifact_part)

        # 5. Upload image bytes directly to public GCS bucket
        storage_client = storage.Client(project=PROJECT_ID)
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(filename)
        blob.upload_from_string(image_bytes, content_type=mime_type)

        public_url = f"https://storage.googleapis.com/{BUCKET_NAME}/{filename}"

        return {
            "status": "success",
            "public_url": public_url,
            "artifact_filename": filename,
            "mime_type": mime_type,
        }
    except Exception as e:
        return f"Error generating or uploading image: {str(e)}"
