export interface IElectronAPI {
  setIgnoreMouseEvents: (ignore: boolean, options?: { forward: boolean }) => void;
  log: (message: string) => void;
  startDrag: () => void;
  stopDrag: () => void;
}

declare global {
  interface Window {
    electronAPI: IElectronAPI;
  }
}

// This extends the React CSS interface to include Electron properties
declare module 'react' {
  interface CSSProperties {
    WebkitAppRegion?: 'drag' | 'no-drag' | 'inherit' | 'initial' | 'unset';
  }
}