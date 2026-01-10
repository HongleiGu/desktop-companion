// eslint-disable-next-line @typescript-eslint/no-require-imports
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  setIgnoreMouseEvents: (ignore, options) =>
    ipcRenderer.send('set-ignore-mouse-events', ignore, options),
  log: (message) => 
    ipcRenderer.send('log-app', message),
  startDrag: () => 
    ipcRenderer.send('window-drag'),
  stopDrag: () => 
    ipcRenderer.send('window-drag-stop'),
});