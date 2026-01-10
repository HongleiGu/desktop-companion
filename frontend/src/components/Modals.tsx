import { Modal } from "antd";
import { useStore } from "../store/store";
import HistoryPanel from "./HistoryPanel";
import UserProfileForm from "./UserProfile";
import PromptEditor from "./PromptEditor";

export default function Modals() {
  const openModal = useStore((s) => s.openModal);
  const setOpenModal = useStore((s) => s.setOpenModal);

  return (
    <>
      <Modal
        open={openModal === "history"}
        onCancel={() => setOpenModal(null)}
        footer={null}
        title="历史记录"
        width={360}
        mask={false}
      >
        <HistoryPanel />
      </Modal>

      <Modal
        open={openModal === "profile"}
        onCancel={() => setOpenModal(null)}
        footer={null}
        title="用户档案"
        width={360}
        mask={false}
      >
        <UserProfileForm />
      </Modal>

      <Modal
        open={openModal === "settings"}
        onCancel={() => setOpenModal(null)}
        footer={null}
        title="设置"
        width={360}
        mask={false}
      >
        <PromptEditor />
      </Modal>
    </>
  );
}
