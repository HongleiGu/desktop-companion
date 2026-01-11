import { Modal } from "antd";
import { useStore } from "../store/store";
import HistoryPanel from "./HistoryPanel";
import UserProfileForm from "./UserProfile";
import PromptEditor from "./PromptEditor";
import ModelConfigPanel from "./ModelConfigPanel";

export default function Modals() {
  const openModal = useStore((s) => s.openModal);
  const setOpenModal = useStore((s) => s.setOpenModal);

  return (
    <>
      {/* History Modal */}
      <Modal
        open={openModal === "history"}
        onCancel={() => setOpenModal(null)}
        footer={null}
        title="历史记录"
        width={360}
        centered
        mask={false}
        // 
      >
        <HistoryPanel />
      </Modal>

      {/* User Profile Modal */}
      <Modal
        open={openModal === "profile"}
        onCancel={() => setOpenModal(null)}
        footer={null}
        title="用户档案"
        width={360}
        centered
        mask={false}
        
      >
        <UserProfileForm />
      </Modal>

      {/* System Prompt Modal */}
      <Modal
        open={openModal === "system prompt"}
        onCancel={() => setOpenModal(null)}
        footer={null}
        title="系统提示词"
        width={1000}
        centered
        mask={false}
        
      >
        <PromptEditor />
      </Modal>

      {/* Model Config Modal */}
      <Modal
        open={openModal === "modelConfig"}
        onCancel={() => setOpenModal(null)}
        footer={null}
        title="模型设置"
        width={1000}
        centered
        mask={false}
        
      >
        <ModelConfigPanel />
      </Modal>
    </>
  );
}
