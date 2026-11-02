Object.defineProperty(exports, Symbol.toStringTag, { value: "Module" });
const require_getQueryKey = require("./getQueryKey-4D2iXfB-.cjs");
const require_shared = require("./shared-BhNi4Oqs.cjs");
let _trpc_server_unstable_core_do_not_import = require("@trpc/server/unstable-core-do-not-import");
let react = require("react");
react = require_getQueryKey.__toESM(react, 1);
//#region src/createTRPCReact.tsx
/**
* @internal
*/
function createHooksInternal(trpc) {
	const proxy = require_shared.createReactDecoration(trpc);
	return (0, _trpc_server_unstable_core_do_not_import.createFlatProxy)((key) => {
		if (key === "useContext" || key === "useUtils") return () => {
			const context = trpc.useUtils();
			return react.useMemo(() => {
				return require_shared.createReactQueryUtils(context);
			}, [context]);
		};
		if (trpc.hasOwnProperty(key)) return trpc[key];
		return proxy[key];
	});
}
function createTRPCReact(opts) {
	return createHooksInternal(require_shared.createRootHooks(opts));
}
//#endregion
//#region src/createTRPCQueryUtils.tsx
function createTRPCQueryUtils(opts) {
	const utils = require_shared.createUtilityFunctions(opts);
	return require_shared.createQueryUtilsProxy(utils);
}
//#endregion
exports.createTRPCQueryUtils = createTRPCQueryUtils;
exports.createTRPCReact = createTRPCReact;
exports.getMutationKey = require_getQueryKey.getMutationKey;
exports.getQueryKey = require_getQueryKey.getQueryKey;
var _trpc_client = require("@trpc/client");
Object.keys(_trpc_client).forEach(function(k) {
	if (k !== "default" && !Object.prototype.hasOwnProperty.call(exports, k)) Object.defineProperty(exports, k, {
		enumerable: true,
		get: function() {
			return _trpc_client[k];
		}
	});
});
