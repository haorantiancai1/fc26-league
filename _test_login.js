const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  const page = await context.newPage();
  
  // 导航到本地测试页面
  await page.goto('http://127.0.0.1:8099/index.html');
  console.log('页面标题:', await page.title());
  
  // 填写登录表单
  await page.fill('#login-name', '阿森纳');
  await page.fill('#login-pass', '123456');
  await page.click('.login-btn');
  
  // 等待导航完成
  await page.waitForTimeout(3000);
  
  // 检查是否登录成功
  const url = page.url();
  console.log('登录后URL:', url);
  
  // 截图
  await page.screenshot({ path: 'E:\\FC26传奇联赛\\deploy\\_login_test.png' });
  console.log('截图已保存到 _login_test.png');
  
  // 检查赵跑跑是否在页面中
  const pageContent = await page.content();
  if (pageContent.includes('赵跑跑')) {
    console.log('✅ 赵跑跑出现在页面中！');
  } else {
    console.log('❌ 未找到赵跑跑');
  }
  
  await browser.close();
})();
