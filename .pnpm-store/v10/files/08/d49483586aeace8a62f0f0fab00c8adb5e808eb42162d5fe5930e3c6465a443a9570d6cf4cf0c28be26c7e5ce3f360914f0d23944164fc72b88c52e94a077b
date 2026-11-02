import { a as _objectSpread2, i as getQueryKeyInternal, o as _objectWithoutProperties } from "../getQueryKey-B1x5Ak4F.mjs";
import { c as getQueryType, t as getQueryClient } from "../shared-DhkLzxq7.mjs";
import { TRPCUntypedClient, getUntypedClient } from "@trpc/client";
import { dehydrate } from "@tanstack/react-query";
import { callProcedure, createFlatProxy, createRecursiveProxy, run } from "@trpc/server/unstable-core-do-not-import";
import { getTransformer } from "@trpc/client/unstable-internals";
//#region src/server/ssgProxy.ts
const _excluded = ["promise"];
/**
* Create functions you can use for server-side rendering / static generation
* @see https://trpc.io/docs/v11/client/nextjs/server-side-helpers
*/
function createServerSideHelpers(opts) {
	const queryClient = getQueryClient(opts);
	const transformer = getTransformer(opts.transformer);
	const resolvedOpts = (() => {
		if ("router" in opts) {
			const { ctx, router } = opts;
			return {
				serialize: (obj) => transformer.output.serialize(obj),
				query: (queryOpts) => {
					return callProcedure({
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
		const untypedClient = client instanceof TRPCUntypedClient ? client : getUntypedClient(client);
		return {
			query: (queryOpts) => untypedClient.query(queryOpts.path, queryOpts.input),
			serialize: (obj) => transformer.output.serialize(obj)
		};
	})();
	function _dehydrate(opts = { shouldDehydrateQuery(query) {
		if (query.state.status === "pending") return false;
		return true;
	} }) {
		const before = run(() => {
			const dehydrated = dehydrate(queryClient, opts);
			return _objectSpread2(_objectSpread2({}, dehydrated), {}, { queries: dehydrated.queries.map((query) => {
				if (query.promise) {
					const { promise: _ } = query;
					return _objectWithoutProperties(query, _excluded);
				}
				return query;
			}) });
		});
		return resolvedOpts.serialize(before);
	}
	const proxy = createRecursiveProxy((opts) => {
		const args = opts.args;
		const input = args[0];
		const arrayPath = [...opts.path];
		const utilName = arrayPath.pop();
		const queryFn = () => resolvedOpts.query({
			path: arrayPath.join("."),
			input
		});
		const queryKey = getQueryKeyInternal(arrayPath, input, getQueryType(utilName));
		return {
			queryOptions: () => {
				const args1 = args[1];
				return _objectSpread2(_objectSpread2({}, args1), {}, {
					queryKey,
					queryFn
				});
			},
			infiniteQueryOptions: () => {
				const args1 = args[1];
				return _objectSpread2(_objectSpread2({}, args1), {}, {
					queryKey,
					queryFn
				});
			},
			fetch: () => {
				const args1 = args[1];
				return queryClient.fetchQuery(_objectSpread2(_objectSpread2({}, args1), {}, {
					queryKey,
					queryFn
				}));
			},
			fetchInfinite: () => {
				var _args1$initialCursor;
				const args1 = args[1];
				return queryClient.fetchInfiniteQuery(_objectSpread2(_objectSpread2({}, args1), {}, {
					queryKey,
					queryFn,
					initialPageParam: (_args1$initialCursor = args1 === null || args1 === void 0 ? void 0 : args1.initialCursor) !== null && _args1$initialCursor !== void 0 ? _args1$initialCursor : null
				}));
			},
			prefetch: () => {
				const args1 = args[1];
				return queryClient.prefetchQuery(_objectSpread2(_objectSpread2({}, args1), {}, {
					queryKey,
					queryFn
				}));
			},
			prefetchInfinite: () => {
				var _args1$initialCursor2;
				const args1 = args[1];
				return queryClient.prefetchInfiniteQuery(_objectSpread2(_objectSpread2({}, args1), {}, {
					queryKey,
					queryFn,
					initialPageParam: (_args1$initialCursor2 = args1 === null || args1 === void 0 ? void 0 : args1.initialCursor) !== null && _args1$initialCursor2 !== void 0 ? _args1$initialCursor2 : null
				}));
			}
		}[utilName]();
	});
	return createFlatProxy((key) => {
		if (key === "queryClient") return queryClient;
		if (key === "dehydrate") return _dehydrate;
		return proxy[key];
	});
}
//#endregion
export { createServerSideHelpers };

//# sourceMappingURL=index.mjs.map