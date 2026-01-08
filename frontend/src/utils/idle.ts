let idleTime = 0;
const IDLE_THRESHOLD = 20 * 60; // 20 minutes

export function startIdleTracker(onIdle: () => void) {
  const resetIdle = () => { idleTime = 0; };
  document.addEventListener("mousemove", resetIdle);
  document.addEventListener("keydown", resetIdle);

  setInterval(() => {
    idleTime++;
    if (idleTime >= IDLE_THRESHOLD) onIdle();
  }, 1000);
}