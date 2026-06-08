/**
 * Converted from Python: core/extract/facades/core_facade.py
 * @generated — WebWeaveX python→javascript library port
 */

import { buildExecutionGraph } from "../../executionGraph.js";
import { computeConfidence } from "../../intelligence/confidenceEngine.js";
import { scoreExtraction, scoreSemanticConfidence, scoreStructureQuality } from "../../quality/index.js";
import { normalizeOutput } from "../../normalize/normalizeOutput.js";
import { deterministicTrace, extractionDiagnostics, performanceMetrics } from "../../observability/index.js";
import { parseSource } from "../../parsers/index.js";

export { buildExecutionGraph, computeConfidence, deterministicTrace, extractionDiagnostics, normalizeOutput, parseSource, performanceMetrics, scoreExtraction, scoreSemanticConfidence, scoreStructureQuality };
