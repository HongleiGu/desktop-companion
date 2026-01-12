import { CharacterProfile } from ".";
import { useStore } from "../store/store";

export interface FrontendToolCall {
  name: string;
  args: Record<string, string>;
  execution: "frontend";
  call_id: string
}

export type FrontendToolHandler = (
  args: Record<string, unknown>
) => void;


export const TOOL_MAP: Record<string, FrontendToolHandler> = {
  update_character_profile: (args) => {
    useStore.getState().setCharacterProfile(args as unknown as CharacterProfile);
  },
  get_character_profile: (args) => {
    return useStore.getState().characterProfile
  }
};
