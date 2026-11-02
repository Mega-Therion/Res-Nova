import { r as getQueryKey, t as getMutationKey } from "./getQueryKey-B1x5Ak4F.mjs";
import { d as createReactDecoration, n as createRootHooks, o as createQueryUtilsProxy, r as createUtilityFunctions, s as createReactQueryUtils } from "./shared-DhkLzxq7.mjs";
import { createFlatProxy } from "@trpc/server/unstable-core-do-not-import";
import * as React from "react";
export * from "@trpc/client";
//#region src/createTRPCReact.tsx
/**
* @internal
*/
function createHooksInternal(trpc) {
	const proxy = createReactDecoration(trpc);
	return createFlatProxy((key) => {
		if (key === "useContext" || key === "useUtils") return () => {
			const context = trpc.useUtils();
			return React.useMemo(() => {
				return createReactQueryUtils(context);
			}, [context]);
		};
		if (trpc.hasOwnProperty(key)) return trpc[key];
		return proxy[key];
	});
}
function createTRPCReact(opts) {
	return createHooksInternal(createRootHooks(opts));
}
//#endregion
//#region src/createTRPCQueryUtils.tsx
function createTRPCQueryUtils(opts) {
	const utils = createUtilityFunctions(opts);
	return createQueryUtilsProxy(utils);
}
//#endregion
export { createTRPCQueryUtils, createTRPCReact, getMutationKey, getQueryKey };

//# sourceMappingURL=index.mjs.map