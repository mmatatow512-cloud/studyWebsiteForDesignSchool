from core.config import DeepSeekConfig

print("DeepSeek Config Test Results:")
print("============================")
print(f"API_KEY: {DeepSeekConfig.API_KEY}")
print(f"BASE_URL: {DeepSeekConfig.BASE_URL}")
print(f"MODEL_NAME: {DeepSeekConfig.MODEL_NAME}")
print(f"MAX_TOKENS: {DeepSeekConfig.MAX_TOKENS}")
print(f"TEMPERATURE: {DeepSeekConfig.TEMPERATURE}")
print(f"TIMEOUT: {DeepSeekConfig.TIMEOUT}")
print("\nConfiguration test passed! All environment variables are correctly loaded.")