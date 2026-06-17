const EMAILJS_SERVICE_ID = "seoul-gajogae-yupum";
const EMAILJS_TEMPLATE_ID = "template_wwbariw";
const EMAILJS_PUBLIC_KEY = "JKsVOKPtnWHIr2BCV";

(function () {
  if (window.emailjs) {
    emailjs.init({ publicKey: EMAILJS_PUBLIC_KEY });
  }
})();

document.addEventListener("DOMContentLoaded", () => {
  const forms = document.querySelectorAll(".consultForm");

  forms.forEach((form) => {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();

      const status = form.querySelector(".status");
      const btn = form.querySelector('button[type="submit"]');

      status.textContent = "";
      status.className = "status";

      const agree = form.querySelector('input[name="agree"]');
      if (!agree || !agree.checked) {
        status.textContent = "개인정보 수집 및 이용에 동의해 주세요.";
        status.classList.add("err");
        return;
      }

      const data = Object.fromEntries(new FormData(form).entries());

      if (!data.name || !data.phone || !data.address) {
        status.textContent = "성함, 연락처, 현장 주소를 입력해 주세요.";
        status.classList.add("err");
        return;
      }

      btn.disabled = true;
      btn.textContent = "접수 중입니다...";

      const messageText = `사이트 : ${data.site_name || "가족애유품정리 서울"}
지역 : ${data.region || "서울"}

연락처 : ${data.phone}

서비스 : ${data.service}

주소 : ${data.address}

상담내용 :
${data.message || ""}

접수시간 :
${new Date().toLocaleString("ko-KR")}`;

      try {
        await emailjs.send(EMAILJS_SERVICE_ID, EMAILJS_TEMPLATE_ID, {
          title: data.title || "[가족애유품정리 서울] 상담접수",
          name: data.name,
          message: messageText
        });

        status.textContent = "상담 접수가 완료되었습니다. 확인 후 연락드리겠습니다.";
        status.classList.add("ok");
        form.reset();
      } catch (err) {
        console.error("EmailJS Error:", err);
        status.textContent = "접수 중 오류가 발생했습니다. 전화 상담을 이용해 주세요.";
        status.classList.add("err");
      } finally {
        btn.disabled = false;
        btn.textContent = "상담 접수하기";
      }
    });
  });
});