function setUserCookie(value) {
  document.cookie = `user_email=${value}`;
}

function setAuthToken(value) {
  document.cookie = `user_token=${value}`;
}

function getUserCookie() {
  const cookieValue = document.cookie.replace(/(?:(?:^|.*;\s*)user_email\s*=\s*([^;]*).*$)|^.*$/, "$1");
  return cookieValue;
}

function getAuthToken() {
  const cookieValue = document.cookie.replace(/(?:(?:^|.*;\s*)user_token\s*=\s*([^;]*).*$)|^.*$/, "$1");
  return cookieValue;
}

function deleteCookie(key) {
  document.cookie = `${key}=; expires=Thu, 01 Jan 1970 00:00:01 GMT;`;
}

export { setUserCookie, setAuthToken, getUserCookie, getAuthToken, deleteCookie }