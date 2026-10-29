// Hide only standalone chrome in a frame, or when explicitly previewing an embed.
// This is presentation only: it does not change the existing password check.
if (window.self !== window.top || new URLSearchParams(location.search).get('embed') === '1') {
  document.documentElement.classList.add('embedded');
}
