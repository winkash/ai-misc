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

