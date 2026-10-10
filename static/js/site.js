/* UI-only localization. Translate backend validation/messages using Django i18n later. */
const translations = {
  fa: {
    features:'ویژگی‌ها',how:'چطور کار می‌کند',login:'ورود',getStarted:'شروع کنید',dashboard:'داشبورد',demoDisclaimer:'پروژه نمایشی • بدون پول واقعی',
    heroEyebrow:'راهی هوشمندانه‌تر برای مدیریت پول',heroTitle:'پول شما.<br><span class="gradient-text">در حرکت.</span>',heroText:'فضایی زیبا برای مدیریت کیف پول دیجیتال، انتقال اعتبار آزمایشی و مشاهده تمام تراکنش‌ها.',exploreFeatures:'مشاهده ویژگی‌ها',instantTransfer:'انتقال فوری',transferComplete:'انتقال موفق',whyFinCore:'چرا فین‌کور',featureHeading:'هر آنچه نیاز دارید.<br>بدون پیچیدگی اضافه.',featureIntro:'ابزارهای ساده و کاربردی برای تجربه بهتر مدیریت پول.',wallet:'کیف پول من',walletDesc:'موجودی شما در یک فضای مرتب و زیبا.',transfer:'انتقال اعتبار',transferDesc:'ارسال اعتبار آزمایشی با روندی ساده و واضح.',transactions:'تراکنش‌ها',historyDesc:'همه فعالیت‌ها را به‌راحتی ببینید.',howHeading:'شروع در سه قدم.',howText:'حساب بسازید، کیف پول را ببینید و انتقال آزمایشی را تجربه کنید.',createAccount:'ساخت حساب',stepOne:'عضویت در فین‌کور',stepOneDesc:'حساب کاربری خود را بسازید.',stepTwo:'دیدن کیف پول',stepTwoDesc:'موجودی و فعالیت آزمایشی را ببینید.',stepThree:'انتقال اعتبار',stepThreeDesc:'بعد از تکمیل بک‌اند، انتقال را امتحان کنید.',
    authWelcome:'به روزهای بهتر مدیریت پول خوش آمدید.',authAside:'کیف پول و تراکنش‌هایتان در یک فضای ساده و آرام.',secureSpace:'فضای امن شما',welcomeBack:'خوش آمدید',loginTitle:'ورود به حساب کاربری',loginSubtitle:'از دیدن دوباره شما خوشحالیم.',username:'نام کاربری',password:'رمز عبور',newHere:'حساب ندارید؟',registerHero:'شروعی تازه برای مدیریت پول.',registerAside:'یک حساب ساده، نمایی روشن از کیف پول آزمایشی.',joinUs:'به فین‌کور بپیوندید',registerTitle:'ساخت حساب کاربری',registerSubtitle:'فقط یک دقیقه زمان می‌برد.',email:'ایمیل',confirmPassword:'تکرار رمز عبور',alreadyAccount:'حساب دارید؟',
    workspace:'بخش کاربری',profile:'پروفایل من',logout:'خروج',demoMode:'حالت آزمایشی',welcome:'خوش برگشتید',overview:'نمای کلی',dashboardIntro:'وضعیت کیف پول در یک نگاه.',totalBalance:'موجودی کل',sampleBalance:'موجودی نمونه؛ متصل به حساب واقعی نیست',moneyIn:'دریافتی',moneyOut:'پرداختی',sampleData:'داده نمونه',recentTransactions:'تراکنش‌های اخیر',activityIntro:'مروری سریع بر فعالیت‌ها.',viewAll:'مشاهده همه ↗',yourMoney:'دارایی شما',walletIntro:'کیف پول آزمایشی در یک جا.',availableBalance:'موجودی قابل استفاده',walletDetails:'جزئیات کیف پول',walletType:'نوع کیف پول',demoWallet:'کیف پول آزمایشی',currency:'واحد پول',status:'وضعیت',payments:'پرداخت‌ها',transferIntro:'تجربه‌ای ساده برای انتقال.',newTransfer:'انتقال جدید',transferDisabled:'انتقال اعتبار تا پیاده‌سازی دفترکل امن در بک‌اند غیرفعال است.',recipient:'نام کاربری گیرنده',amount:'مبلغ (دلار)',note:'توضیح (اختیاری)',sendTransfer:'ارسال اعتبار',builtWithCare:'طراحی اصولی',transferTip:'انتقال واقعی با تراکنش دیتابیس و بررسی موجودی پیاده‌سازی می‌شود.',yourActivity:'فعالیت‌های شما',transactionsIntro:'گزارشی روشن از دریافت‌ها و پرداخت‌ها.',transactionHistory:'تاریخچه تراکنش‌ها',account:'حساب کاربری',profileIntro:'اطلاعات حساب خود را به‌روز نگه دارید.',personalAccount:'حساب شخصی',firstName:'نام',lastName:'نام خانوادگی',saveChanges:'ذخیره تغییرات'
  }
};
const originalText = new Map();
function setLanguage(lang) {
  lang = lang === 'fa' ? 'fa' : 'en';
  document.documentElement.lang = lang;
  document.documentElement.dir = lang === 'fa' ? 'rtl' : 'ltr';
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.dataset.i18n;
    if (!originalText.has(el)) originalText.set(el, el.innerHTML);
    el.innerHTML = lang === 'fa' && translations.fa[key] ? translations.fa[key] : originalText.get(el);
  });
  document.querySelectorAll('[data-lang]').forEach(btn => {
    const active = btn.dataset.lang === lang;
    btn.classList.toggle('active', active);
    btn.setAttribute('aria-pressed', String(active));
  });
  try { localStorage.setItem('fincore-language', lang); } catch (_) {}
}
document.addEventListener('DOMContentLoaded', () => {
  let lang = 'en';
  try { lang = localStorage.getItem('fincore-language') || 'en'; } catch (_) {}
  document.querySelectorAll('[data-lang]').forEach(btn => btn.addEventListener('click', () => setLanguage(btn.dataset.lang)));
  setLanguage(lang);
});
