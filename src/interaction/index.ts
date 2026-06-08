/**
 * Barrel converted from core/interaction/__init__.py
 * @generated — WebWeaveX python→javascript library port
 */

export { buildInteractionPlan, clickElement, fillInput, hoverElement, recordInteraction, selectOption, waitForSelector } from "./browserInteractionEngine.js";
export { extractInfiniteScroll } from "./infiniteScrollEngine.js";
export { buildInteractionGraph, interactionGraphToRuntimeIr } from "./interactionGraphEngine.js";
export { replayInteractions } from "./interactionReplayEngine.js";
export { loadInteractionReplay, saveInteractionReplay } from "./interactionReplayStore.js";
export { closeModal, detectModals } from "./modalRuntimeEngine.js";
export { extractPaginatedContent } from "./paginationEngine.js";
export { captureTabs, switchTab } from "./tabRuntimeEngine.js";
