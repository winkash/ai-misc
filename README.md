# ai-misc
Miscellaneous utilities in AI 
1. Building a Coding Agent From Scratch
<img width="753" height="385" alt="image" src="https://github.com/user-attachments/assets/af654cf1-47e4-4690-a915-1c4d3d8680a5" />

#  Terminology
- System prompt
  - Define the behavior and some directives for the overall LLM
- User prompt
- Custom user requests
  - Assistant prompt
  - LLM’s response

#  Steps
- Read in terminal and keep appending to conversation
- Tell LLM what tools are available
  - It asks for tool use at appropriate time
  - You execute tool offline and return response
  - “Read_file”
  - “List_dir”
  - “Edit_file”
- Create a new file, edit a new file

2. Adding a KVCache to LLM Inference to improce latency
   <img width="3322" height="1320" alt="image" src="https://github.com/user-attachments/assets/de616065-c379-42bc-8c32-586c00fa8583" />
   
#  Steps
1. First Generation: When the model sees the first input, it calculates and stores its keys and values in the cache
2. Next Words: For each new word, the model retrieves the stored keys and values and adds the new ones instead of starting over.
3. Efficient Attention Computation: calculate attention using the cached K and V along with the new Q (query) to compute the output.
4. Update Input: add the newly generated token to the input and go back to step 2 until we finish generating


