import { app, BrowserWindow, ipcMain, screen } from 'electron';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import isDev from 'electron-is-dev';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    frame: false,
    transparent: true,
    alwaysOnTop: true,
    resizable: false,
    hasShadow: false,
    webPreferences: {
      preload: join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
    },
  });

  const url = isDev ? 'http://localhost:3000' : `file://${join(__dirname, '../../out/index.html')}`;
  mainWindow.loadURL(url);
}

// Robust Manual Dragging Logic
ipcMain.on('window-drag', (event) => {
  const win = BrowserWindow.fromWebContents(event.sender);
  if (!win) return;

  const { x: startMouseX, y: startMouseY } = screen.getCursorScreenPoint();
  const [startWinX, startWinY] = win.getPosition();

  const dragInterval = setInterval(() => {
    if (win.isDestroyed()) {
      clearInterval(dragInterval);
      return;
    }
    const { x, y } = screen.getCursorScreenPoint();
    win.setPosition(
      startWinX + (x - startMouseX),
      startWinY + (y - startMouseY)
    );
  }, 10); // 10ms for 100fps smooth movement

  ipcMain.once('window-drag-stop', () => {
    clearInterval(dragInterval);
  });
});

ipcMain.on('set-ignore-mouse-events', (event, ignore, options) => {
  const win = BrowserWindow.fromWebContents(event.sender);
  win?.setIgnoreMouseEvents(ignore, options || { forward: true });
});

app.whenReady().then(createWindow);