# InterAuto_Candyabc
【接口】关键字驱动+Pytest参数化+Allure测试报告
## 代码结构
```python
> commom:     通用配置
> config:     配置文件
> data:       测试数据
> logs:       日志目录
> report:     测试报告
> testcase:   测试用例
> utils:      工具类包
> pytest.ini: pytest配置
> run.py:     主运行
```
## 接口测试框架流程
```python
> 主程序运行（pytest框架）
> Excel用例（数据驱动）
> 配置文件（yaml）
> Request
> 断言（结果断言，数据库验证）
> 报告（Allure）
> 邮件
```
