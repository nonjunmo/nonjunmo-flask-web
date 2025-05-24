let current = new Date();

function renderCalendar() {
  const monthSpan = document.getElementById('current-month');
  const calendar = document.getElementById('calendar');
  const today = new Date();
  calendar.innerHTML = '';
  const y = current.getFullYear(), m = current.getMonth();
  monthSpan.textContent = y + '년 ' + (m + 1) + '월';
  const firstDay = new Date(y, m, 1).getDay();
  const lastDate = new Date(y, m + 1, 0).getDate();

  let html = '<tr><th>일</th><th>월</th><th>화</th><th>수</th><th>목</th><th>금</th><th>토</th></tr><tr>';
  for (let i = 0; i < firstDay; i++) html += '<td></td>';
  for (let d = 1; d <= lastDate; d++) {
    const day = new Date(y, m, d);
    const isSat = day.getDay() === 6;
    const isSun = day.getDay() === 0;
    const isToday = day.toDateString() === today.toDateString();
    const className = (isSat || isSun ? 'weekend ' : '') + (isToday ? 'today' : '');
    html += `<td class="${className}" onclick="showForm('${y}-${m+1}-${d}')">${d}</td>`;
    if ((i + d) % 7 === 0) html += '</tr><tr>';
  }
  html += '</tr>';
  calendar.innerHTML = html;
}

function changeMonth(offset) {
  current.setMonth(current.getMonth() + offset);
  renderCalendar();
}

function showForm(date) {
  document.getElementById('application-form').style.display = 'block';
  document.getElementById('selected-date').value = date;
}
function hideForm() {
  document.getElementById('application-form').style.display = 'none';
}

function submitApplication(e) {
  e.preventDefault();
  const form = e.target;
  const data = new URLSearchParams(new FormData(form));
  fetch('/apply', {
    method: 'POST',
    body: data
  }).then(res => res.json()).then(result => {
    if (result.success) {
      alert('신청 완료!');
      hideForm();
    }
  });
}

window.onload = renderCalendar;