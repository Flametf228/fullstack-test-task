import { Alert, Button, Form, Modal } from "react-bootstrap";
import { useUploadForm } from "@/hooks/useUploadForm";

export function UploadModal({
  show,
  onHide,
  onUploaded,
}: {
  show: boolean;
  onHide: () => void;
  onUploaded: () => void;
}) {
  const form = useUploadForm(() => {
    onUploaded();
    onHide();
  });

  return (
    <Modal show={show} onHide={onHide} centered>
      <Form
        onSubmit={(event) => {
          event.preventDefault();
          void form.submit();
        }}
      >
        <Modal.Header closeButton>
          <Modal.Title>Добавить файл</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {form.error ? <Alert variant="danger">{form.error}</Alert> : null}
          <Form.Group className="mb-3">
            <Form.Label>Название</Form.Label>
            <Form.Control
              value={form.title}
              onChange={(event) => form.setTitle(event.target.value)}
              placeholder="Например, Договор с подрядчиком"
            />
          </Form.Group>
          <Form.Group>
            <Form.Label>Файл</Form.Label>
            <Form.Control
              type="file"
              onChange={(event) =>
                form.setFile((event.target as HTMLInputElement).files?.[0] ?? null)
              }
            />
          </Form.Group>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="outline-secondary" onClick={onHide}>
            Отмена
          </Button>
          <Button type="submit" variant="primary" disabled={form.isSubmitting}>
            {form.isSubmitting ? "Загрузка..." : "Сохранить"}
          </Button>
        </Modal.Footer>
      </Form>
    </Modal>
  );
}
