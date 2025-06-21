from transformers import AutoTokenizer, AutoModelForCausalLM

model_name = "microsoft/DialoGPT-small"
save_dir = "./pretrained/dialo"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

tokenizer.save_pretrained(save_dir)
model.save_pretrained(save_dir)

print("Download finished! Model files:", os.listdir(save_dir))




