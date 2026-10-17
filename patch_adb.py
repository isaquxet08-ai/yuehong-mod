import os

file_path = "manager/src/main/kotlin/roro/stellar/manager/ui/features/manager/StarterScreen.kt"
if not os.path.exists(file_path):
    print("❌ 找不到 StarterScreen.kt，请确认当前目录！")
    exit(1)

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

target_str = 'updateStep(1, StepStatus.WARNING, context.getString(R.string.need_pairing))'

replacement_str = '''// [Android 10 向下兼容补丁] 自动注入
if (android.os.Build.VERSION.SDK_INT < 30) {
    try {
        // 安卓10及以下直接走本地端口，不需要配对码
        roro.stellar.manager.adb.UsbAdbClient.executeRawService("tcpip:5555")
        roro.stellar.manager.adb.UsbAdbClient.executeRawService("connect:127.0.0.1:5555")
        updateStep(1, StepStatus.COMPLETED, "Android 10 已通过本地端口 5555 连接")
    } catch (e: Exception) {
        updateStep(1, StepStatus.ERROR, "本地连接失败: ${e.message}")
    }
} else {
    // 安卓11及以上走原有的配对逻辑
    updateStep(1, StepStatus.WARNING, context.getString(R.string.need_pairing))
}'''

if target_str in content:
    content = content.replace(target_str, replacement_str)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ 代码修改成功！安卓10兼容逻辑已注入。")
else:
    print("❌ 没找到目标代码，可能源码版本不同。")
