export function celebrate() {
  try {
    if (window.confetti) {
      window.confetti({ particleCount: 120, spread: 70, origin: { y: 0.6 } });
    }
  } catch (_) {}
}