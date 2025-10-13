from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained('HuggingFaceTB/SmolLM2-1.7B')
model = AutoModelForCausalLM.from_pretrained('HuggingFaceTB/SmolLM2-1.7B').cuda()

tokens = tokenizer("Hello, how are you?", return_tensors="pt").cuda()
outputs = model.generate(**tokens, max_new_tokens=300, use_cache=True)
output_text = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
print(output_text)
