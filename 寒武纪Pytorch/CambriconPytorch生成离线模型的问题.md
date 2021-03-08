Cambricon Pytorch需要借助torch.jit模块生成离线模型，范例如下：
```
# 模型持久化，此处生成的模型文件运行还需要借助pytorch框架
model.eval().float().mlu()
model.set_core_number(core_number)
example_input = torch.randn(batch_size, channel, h, w).mlu()
traced_model = torch.jit.trace(model, torch.randn(1, channel, h, w).mlu())
traced_model(example_input)
traced_model.save("model.pt")
new_traced_model = torch.jit.load("model.pt")

# 生成Cambricon格式的离线模型
model.eval().float().mlu()
model.set_core_number(core_number)
example_input = torch.randn(batch_size, channel, h, w).mlu()
traced_model = torch.jit.trace(model, torch.randn(1, channel, h, w).mlu(), check_trace=False)
traced_model(example_input)
traced_model.save(model_name, True)  # 生成后缀为cambricon格式的离线模型文件
```
注意：
1. 在调用save之前最少前向推理一次
2. 最后生成离线模型的输入尺寸与推理时的example_input尺寸一致
3. 使用load加载离线模型后不可以再次保存new_traced_model
4. 使用save生成Cambricon格式的离线文件时需要指定第二个参数为True