Object.defineProperty(exports, Symbol.toStringTag, { value: "Module" });
const require_getQueryKey = require("../getQueryKey-4D2iXfB-.cjs");
const require_shared = require("../shared-BhNi4Oqs.cjs");
let _trpc_client = require("@trpc/client");
let _tanstack_react_query = require("@tanstack/react-query");
let _trpc_server_unstable_core_do_not_import = require("@trpc/server/unstable-core-do-not-import");
let _trpc_client_unstable_internals = require("@trpc/client/unstable-internals");
//#region src/server/ssgProxy.ts
const _excluded = ["promise"];
/**
* Create functions you can use for server-side rendering / static generation
* @see https://trpc.io/docs/v11/client/nextjs/server-side-helpers
*/
function createServerSideHelpers(opts) {
	const queryClient = require_shared.getQueryClient(opts);
	const transformer = (0, _trpc_client_unstable_internals.getTransformer)(opts.transformer);
	const resolvedOpts = (() => {
		if ("router" in opts) {
			const { ctx, router } = opts;
			return {
				serialize: (obj) => transformer.output.serialize(obj),
				query: (queryOpts) => {
					return (0, _trpc_server_unstable_core_do_not_import.callProcedure)({
						router,
						path: queryOpts.path,
						getRawInput: async () => queryOpts.input,
						ctx,
						type: "query",
						signal: void 0,
						batchIndex: 0
					});
				}
			};
		}
		const { client } = opts;
		const untypedClient = client instanceof _trpc_client.TRPCUntypedClient ? client : (0, _trpc_client.getUntypedClient)(client);
		return {
			query: (queryOpts) => untypedClient.query(queryOpts.path, queryOpts.input),
			serialize: (obj) => transformer.output.serialize(obj)
		};
	})();
	function _dehydrate(opts = { shouldDehydrateQuery(query) {
		if (query.state.status === "pending") return false;
		return true;
	} }) {
		const before = (0, _trpc_server_unstable_core_do_not_import.run)(() => {
			const dehydrated = (0, _tanstack_react_query.dehydrate)(queryClient, opts);
			return require_getQueryKey._objectSpread2(require_getQueryKey._objectSpread2({}, dehydrated), {}, { queries: dehydrated.queries.map((query) => {
				if (query.promise) {
					const { promise: _ } = query;
					return require_getQueryKey._objectWithoutProperties(query, _excluded);
				}
				return query;
			}) });
		});
		return resolvedOpts.serialize(before);
	}
	const proxy = (0, _trpc_server_unstable_core_do_not_import.createRecursiveProxy)((opts) => {
		const args = opts.args;
		const input = args[0];
		const arrayPath = [...opts.path];
		const utilName = arrayPath.pop();
		const queryFn = () => resolvedOpts.query({
			path: arrayPath.join("."),
			input
		});
		const queryKey = require_getQueryKey.getQueryKeyInternal(arrayPath, input, require_shared.getQueryType(utilName));
		return {
			queryOptions: () => {
				const args1 = args[1];
				return require_getQueryKey._objectSpread2(require_getQueryKey._objectSpread2({}, args1), {}, {
					queryKey,
					queryFn
				});
			},
			infiniteQueryOptions: () => {
				const args1 = args[1];
				return require_getQueryKey._objectSpread2(require_getQueryKey._objectSpread2({}, args1), {}, {
					queryKey,
					queryFn
				});
			},
			fetch: () => {
				const args1 = args[1];
				return queryClient.fetchQuery(require_getQueryKey._objectSpread2(require_getQueryKey._objectSpread2({}, args1), {}, {
					queryKey,
					queryFn
				}));
			},
			fetchInfinite: () => {
				var _args1$initialCursor;
				const args1 = args[1];
				return queryClient.fetchInfiniteQuery(require_getQueryKey._objectSpread2(require_getQueryKey._objectSpread2({}, args1), {}, {
					queryKey,
					queryFn,
					initialPageParam: (_args1$initialCursor = args1 === null || args1 === void 0 ? void 0 : args1.initialCursor) !== null && _args1$initialCursor !== void 0 ? _args1$initialCursor : null
				}));
			},
			prefetch: () => {
				const args1 = args[1];
				return queryClient.prefetchQuery(require_getQueryKey._objectSpread2(require_getQueryKey._objectSpread2({}, args1), {}, {
					queryKey,
					queryFn
				}));
			},
			prefetchInfinite: () => {
				var _args1$initialCursor2;
				const args1 = args[1];
				return queryClient.prefetchInfiniteQuery(require_getQueryKey._objectSpread2(require_getQueryKey._objectSpread2({}, args1), {}, {
					queryKey,
					queryFn,
					initialPageParam: (_args1$initialCursor2 = args1 === null || args1 === void 0 ? void 0 : args1.initialCursor) !== null && _args1$initialCursor2 !== void 0 ? _args1$initialCursor2 : null
				}));
			}
		}[utilName]();
	});
	return (0, _trpc_server_unstable_core_do_not_import.createFlatProxy)((key) => {
		if (key === "queryClient") return queryClient;
		if (key === "dehydrate") return _dehydrate;
		return proxy[key];
	});
}
//#endregion
exports.createServerSideHelpers = createServerSideHelpers;
