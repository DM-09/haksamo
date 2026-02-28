function getAPI(url, type='txt') {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest()
    xhr.open('GET', url, true)
    xhr.responseType = type

    xhr.onload = function() {
      if (xhr.status >= 200 && xhr.status < 300) {
		var res = xhr.response
        resolve(res)
      } else {
        reject(new Error(`Request failed with status ${xhr.status}`))
      }
    }

    xhr.onerror = function() { reject(new Error('Network error')) }
    xhr.send()
  })
}


async function start() {
  var url = document.querySelector('#url').value
  var host = url.split('://')[1].replace('/', '')
  
  var el = document.querySelector('#link')
  el.innerHTML = '<가져오는 중> <br><br>'
  
  var res = await getAPI('/api/get_mi?host='+host)
  
  if (res == 'error') {
    el.innerHTML = '< URL이 올바르지 않거나 지원하지 않는 학교입니다. > <br><br>'
  } else {
    el.innerHTML = `ics 링크: https://haksamo.vercel.app/cal?host=${host}&mi=${res} <br><a href='#' onClick="window.open('https://share.google/aimode/EBAccMJ5ViUuWCyxP')">캘린더에 추가하는 방법</a><br><br>`
  }
}
