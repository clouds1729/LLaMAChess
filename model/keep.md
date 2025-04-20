---

### 📦 Add the Model (Not Included)

The LLaMA model file is **not included** in this repository due to its size.

To run the backend, you’ll need to:

1. **Download a `.gguf` model file** from Hugging Face:  
   👉 [LLaMA 2 7B Chat GGUF (q4_K_M)](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf)

2. **Ensure the file size is over 3GB** (this confirms it's the full model).

3. Rename the file to:

   ```
   llama.gguf
   ```

4. Move it into your project folder:

   ```
   backend/models/llama.gguf
   ```

5. Then start the backend server:

   ```bash
   uvicorn main:app --reload
   ```

---

