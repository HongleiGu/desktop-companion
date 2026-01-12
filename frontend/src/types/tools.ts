import { CharacterProfile } from ".";
import { useStore } from "../store/store";

export interface FrontendToolCall {
  name: string;
  args: Record<string, string>;
  execution: "frontend";
  call_id: string
}

export type FrontendToolHandler = (
  args: unknown
) => {
  message: string,
  value: unknown
};


export const TOOL_MAP: Record<string, FrontendToolHandler> = {
  update_character_profile: (args) => {
    useStore.getState().setCharacterProfile(args as unknown as CharacterProfile);
    return {
      message: "Charater Profile Updated",
      value: null
    }
  },
  get_character_profile: (args) => {
    return {
      message: "Character Profile fetched successfully",
      value: useStore.getState().characterProfile
    }
  }
};
