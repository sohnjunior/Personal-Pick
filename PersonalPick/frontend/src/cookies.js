function setUserCookie(value) {
  document.cookie = `user_email=${value}`;
}

function getUserCookie() {
  const cookieValue = document.cookie.replace(/(?:(?:^|.*;\s*)user_email\s*=\s*([^;]*).*$)|^.*$/, "$1");
  return cookieValue;
}

function deleteCookie(key) {
  document.cookie = `${key}=; expires=Thu, 01 Jan 1970 00:00:01 GMT;`;
}

export { setUserCookie, getUserCookie, deleteCookie }