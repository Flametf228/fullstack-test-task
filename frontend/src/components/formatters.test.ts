import { describe, expect, it } from "vitest";
import {
  formatSize,
  getLevelVariant,
  getProcessingVariant,
  isInFlight,
} from "@/components/formatters";
import type { FileItem } from "@/types/file";

describe("formatSize", () => {
  it("отдаёт байты как есть", () => expect(formatSize(512)).toBe("512 B"));
  it("переводит в килобайты", () => expect(formatSize(2048)).toBe("2.0 KB"));
  it("переводит в мегабайты", () =>
    expect(formatSize(5 * 1024 * 1024)).toBe("5.0 MB"));
  it("держит границу килобайта", () => expect(formatSize(1024)).toBe("1.0 KB"));
});

describe("getLevelVariant", () => {
  it("critical -> danger", () => expect(getLevelVariant("critical")).toBe("danger"));
  it("warning -> warning", () => expect(getLevelVariant("warning")).toBe("warning"));
  it("остальное -> success", () => expect(getLevelVariant("info")).toBe("success"));
});

describe("getProcessingVariant", () => {
  it("failed -> danger", () => expect(getProcessingVariant("failed")).toBe("danger"));
  it("processing -> warning", () =>
    expect(getProcessingVariant("processing")).toBe("warning"));
  it("processed -> success", () =>
    expect(getProcessingVariant("processed")).toBe("success"));
  it("uploaded -> secondary", () =>
    expect(getProcessingVariant("uploaded")).toBe("secondary"));
});

describe("isInFlight", () => {
  const base = { processing_status: "uploaded" } as FileItem;

  it("uploaded ещё в работе", () => expect(isInFlight(base)).toBe(true));
  it("processing ещё в работе", () =>
    expect(isInFlight({ ...base, processing_status: "processing" })).toBe(true));
  it("processed завершён", () =>
    expect(isInFlight({ ...base, processing_status: "processed" })).toBe(false));
  it("failed завершён", () =>
    expect(isInFlight({ ...base, processing_status: "failed" })).toBe(false));
});
