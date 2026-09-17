# 5 AstraBuild method

AstraBuild treats component-level site reconstruction as a persistent programmatic process rather than a single inference from images to geometry. The workflow combines a general-purpose reasoning model, executable Blender/Python procedures, registered physical evidence, task-specific validation, and an inherited engineering state. The model configuration is owner-confirmed as GPT-6 Astra accessed through Codex; the historical B01–B36 artifacts preserve the resulting programs, plans, diagnostics, and validation outputs, but not the model's private reasoning trace. Our analysis therefore concerns observable model-in-harness actions and saved artifacts.

## 5.1 Evidence and persistent target state

Each batch starts from a subset of four evidence sources: registered photogrammetric geometry, UAV or ground imagery, engineering or inventory records when available, and the accepted reconstruction state inherited from earlier batches. The photogrammetric reference supplies a common spatial frame and local surface evidence, but it is not treated as an independent survey reference or as a complete segmentation of physical components. Images are used to resolve appearance, component structure, and regions where the registered geometry is missing or ambiguous. Engineering records provide identity or configuration information when those mappings are supported.

The target is an editable component-level Blender state rather than a fused surface. It may contain reusable component collections, rigid site instances, finite site-specific connections, curves or conductor paths, civil geometry, and validation/provenance records. Accepted geometry remains available to later batches. Historical versions are retained instead of being silently overwritten, allowing later tasks to reuse prior components while preserving earlier evidence and failure states.

## 5.2 Division of labor between model and deterministic geometry tools

The workflow separates problem formulation from numerical geometry. Observable model-side actions include selecting the relevant evidence and spatial domain, choosing a geometric representation, decomposing a target into reusable and site-specific parts, authoring or revising Blender/Python procedures, selecting measurement or routing operators, and interpreting validation or review outputs when deciding what to revise. These actions are visible through the generated plans, scripts, revision records, and saved program variants.

Numerical computation is performed by explicit deterministic procedures. Depending on the task, these include geometric fitting, coordinate transforms, profile or spline computation, mesh construction, rendering, surface-distance calculations, endpoint/contact/continuity checks, collision checks, and state-preservation tests. Validators reopen saved files and recompute scoped checks rather than relying only on the builder's in-memory state. Quantitative residuals therefore characterize the output of explicit geometry procedures selected and executed within the workflow; they should not be interpreted as the language model directly performing high-precision numerical optimization.

## 5.3 Persistent reconstruction loop

At batch \(t\), the workflow can be summarized as

\[
(E_t, S_{t-1}) \rightarrow O_t \rightarrow G_t \rightarrow V_t \rightarrow S_t,
\]

where \(E_t\) is the evidence selected for the current task, \(S_{t-1}\) is the previously accepted engineering state, \(O_t\) is an executable reconstruction operation formulated through the model/harness, \(G_t\) is the resulting saved geometry and process evidence, and \(V_t\) is task-specific validation or review. Validation can retain the update, expose a local mismatch, or motivate a revised operation. The accepted result becomes part of \(S_t\) and can be addressed by subsequent batches through named collections, transforms, ports, and endpoints.

The validation criterion depends on the represented geometry. Local rigid structures may use scoped surface comparisons; connected systems additionally require endpoint and contact constraints; omission discovery uses selected-region coverage; late batches check preservation of inherited transforms and, where needed, geometric interference. This heterogeneity is intentional: no single residual is used as a universal station-wide accuracy measure.

## 5.4 Worked trace: changing the representation in B23

B23 illustrates the separation between representation choice and numerical fitting. The inherited preflight treated a transformer neutral connection primarily as a straight two-end problem. Inspection of the registered reference showed a lateral bow of roughly 0.5 m through the middle of the trajectory, indicating that the straight representation omitted observed source geometry. The reconstruction operation was reformulated as a constrained curved path. Source geometry was spatially binned, eight control points were extracted, and deterministic code fit a cubic B-spline with fixed endpoints and a smoothness penalty. The saved path terminated at the existing B08 transformer terminal interface and was evaluated with finite source domains and endpoint checks.

The first revised geometry did not explain all nearby structure. Subsequent B23 revisions added soft connections and lower bridge contact while preserving the earlier state and fixed comparison domains. The method-level point is the ordering of decisions: the workflow first changes the geometric hypothesis from a straight segment to a curved path; numerical fitting then estimates parameters within that representation; validation tests the saved result and can trigger another local revision. This pattern recurs elsewhere in B01–B36 with different operators, including reusable-scope revisions in B15 and route/interference revisions in B20 and B36.
