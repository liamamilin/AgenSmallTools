

### 使用方式

1. 准备 `input.csv`：

   ```
   id,user_prompt
   1,什么是二次函数？
   2,请解释概率的含义
   ```

2. 运行命令：

   ```bash
   python batch_runner.py input.csv output.csv
   ```

3. 结果会保存在 `output.csv`：

   ```
   id,user_prompt,result
   1,什么是二次函数？,二次函数是 y=ax^2+bx+c 的形式...
   2,请解释概率的含义,概率是事件发生可能性的度量...
   ```

---

要不要我帮你再加一个 **进度条（tqdm）**？这样批量调用时用户能看到进度，比如 “处理 1/1000 …”。
