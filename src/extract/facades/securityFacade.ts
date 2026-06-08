/**
 * Converted from Python: core/extract/facades/security_facade.py
 * @generated — WebWeaveX python→javascript library port
 */

import { isSafeRemoteTarget } from "../../security/remoteTarget.js";
import { enforceResourceBudget } from "../../security/resourceBudget.js";
import { decompressionGuard, malformedPayloadGuard, memoryGuard, recursionGuard, redirectGuard, sandboxText, ssrfGuard, timeoutGuard } from "../../security/hardening/index.js";
import { budgetedChunks, incrementalParse, lazyExtract, memoryBudget, parserPool, streamParse } from "../../performance/index.js";

export { budgetedChunks, decompressionGuard, enforceResourceBudget, incrementalParse, isSafeRemoteTarget, lazyExtract, malformedPayloadGuard, memoryBudget, memoryGuard, parserPool, recursionGuard, redirectGuard, sandboxText, ssrfGuard, streamParse, timeoutGuard };
