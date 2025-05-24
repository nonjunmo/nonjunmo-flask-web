
document.addEventListener('DOMContentLoaded', function () {
  const calendarEl = document.getElementById('calendar');
  const monthLabel = document.getElementById('month-label');
  const prevBtn = document.getElementById('prev-month');
  const nextBtn = document.getElementById('next-month');
  const applyForm = document.getElementById('application-form');
  const applyDateInput = document.getElementById('apply-date');
  let current = new Date();
  current.setDate(1);
  let openedDate = null;

  function isToday(date) {
    const today = new Date();
    const d1 = new Date(today.getFullYear(), today.getMonth(), today.getDate());
    const d2 = new Date(date.getFullYear(), date.getMonth(), date.getDate());
    return d1.getTime() === d2.getTime();
  }

  function renderCalendar(dateObj) {
    calendarEl.innerHTML = "";

    const weekdayRow = document.createElement('div');
    weekdayRow.className = 'weekday-header';
    ['일', '월', '화', '수', '목', '금', '토'].forEach(day => {
      const dayEl = document.createElement('div');
      dayEl.textContent = day;
      weekdayRow.appendChild(dayEl);
    });
    calendarEl.appendChild(weekdayRow);

    const grid = document.createElement('div');
    grid.className = 'calendar-grid';

    const year = dateObj.getFullYear();
    const month = dateObj.getMonth();
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);

    for (let i = 0; i < firstDay.getDay(); i++) {
      grid.innerHTML += '<div class="day empty"></div>';
    }

    for (let day = 1; day <= lastDay.getDate(); day++) {
      const d = new Date(year, month, day);
      const yyyyMMdd = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
      const dayEl = document.createElement('div');
      dayEl.className = 'day';
      dayEl.textContent = day;

      if (isToday(d)) {
        dayEl.classList.add('today');
      }

      const now = new Date();
      const isPastSaturday = d < now && d.getDay() === 6;
      const isFridayAfterFive = now.getDay() === 5 && now.getHours() >= 17 &&
                                 d.getDay() === 6 &&
                                 d.getFullYear() === now.getFullYear() &&
                                 d.getMonth() === now.getMonth() &&
                                 d.getDate() === now.getDate() + 1;

      if (isPastSaturday || isFridayAfterFive) {
        dayEl.classList.add('closed');
        dayEl.style.pointerEvents = 'none';
      }

      if (d.getDay() === 6) {
        dayEl.classList.add('weekend');
        fetch(`/get_count/${yyyyMMdd}`).then(res => res.json()).then(data => {
          const count = data.count;
          const status = document.createElement('span');
          status.className = 'status';
          if (count === 0) {
            status.textContent = "신청중";
          } else if (count < 5) {
            status.textContent = `신청중 (${count})`;
          } else {
            status.textContent = "마감";
            dayEl.classList.add("full");
          }
          dayEl.appendChild(status);
        });

        dayEl.addEventListener('click', () => {
          if (openedDate === yyyyMMdd) {
            applyForm.style.display = 'none';
            openedDate = null;
            return;
          }
          openedDate = yyyyMMdd;
          applyDateInput.value = yyyyMMdd;
          applyForm.style.display = 'block';
        });
      }

      grid.appendChild(dayEl);
    }

    calendarEl.appendChild(grid);
    monthLabel.textContent = `${year}년 ${month + 1}월`;
  }

  document.getElementById('cancel-button').addEventListener('click', () => {
    applyForm.style.display = 'none';
    openedDate = null;
  });

  document.getElementById('apply-form').addEventListener('submit', function (e) {
    e.preventDefault();
    const formData = new FormData(this);
    const jsonData = {};
    formData.forEach((value, key) => { jsonData[key] = value });
    fetch('/apply', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(jsonData)
    }).then(res => res.json()).then(data => {
      if (data.status === 'success') {
        alert(`${jsonData.name}님, ${jsonData.date} 신청 완료되었습니다.`);
        applyForm.style.display = 'none';
        openedDate = null;
        renderCalendar(current);
      }
    });
  });

  prevBtn.addEventListener('click', () => {
    current.setMonth(current.getMonth() - 1);
    renderCalendar(current);
  });

  nextBtn.addEventListener('click', () => {
    current.setMonth(current.getMonth() + 1);
    renderCalendar(current);
  });

  renderCalendar(current);
});
