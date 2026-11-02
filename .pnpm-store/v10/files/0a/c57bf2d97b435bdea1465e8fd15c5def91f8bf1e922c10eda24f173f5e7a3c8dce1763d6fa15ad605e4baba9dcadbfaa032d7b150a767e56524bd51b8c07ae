Object.defineProperty(exports, Symbol.toStringTag, { value: "Module" });
const require_getQueryKey = require("./getQueryKey-4D2iXfB-.cjs");
let _tanstack_react_query = require("@tanstack/react-query");
let _trpc_server_unstable_core_do_not_import = require("@trpc/server/unstable-core-do-not-import");
let react = require("react");
react = require_getQueryKey.__toESM(react, 1);
//#region src/rsc.tsx
const HELPERS = ["prefetch", "prefetchInfinite"];
/**
* @note This requires `@tanstack/react-query@^5.49.0`
* @note Make sure to have `dehydrate.serializeData` and `hydrate.deserializeData`
* set to your data transformer in your `QueryClient` factory.
* @example
* ```ts
* export const createQueryClient = () =>
*   new QueryClient({
*     defaultOptions: {
*       dehydrate: {
*         serializeData: transformer.serialize,
*       },
*       hydrate: {
*         deserializeData: transformer.deserialize,
*       },
*     },
*   });
* ```
*/
function createHydrationHelpers(caller, getQueryClient) {
	const wrappedProxy = (0, _trpc_server_unstable_core_do_not_import.createRecursiveProxy)(async (opts) => {
		const path = [...opts.path];
		const args = [...opts.args];
		const proc = path.reduce((acc, key) => HELPERS.includes(key) ? acc : acc[key], caller);
		const input = args[0];
		const promise = proc(input);
		const helper = path.pop();
		if (helper === "prefetch") {
			const args1 = args[1];
			return getQueryClient().prefetchQuery(require_getQueryKey._objectSpread2(require_getQueryKey._objectSpread2({}, args1), {}, {
				queryKey: require_getQueryKey.getQueryKeyInternal(path, input, "query"),
				queryFn: () => promise
			}));
		}
		if (helper === "prefetchInfinite") {
			var _args1$initialCursor;
			const args1 = args[1];
			return getQueryClient().prefetchInfiniteQuery(require_getQueryKey._objectSpread2(require_getQueryKey._objectSpread2({}, args1), {}, {
				queryKey: require_getQueryKey.getQueryKeyInternal(path, input, "infinite"),
				queryFn: () => promise,
				initialPageParam: (_args1$initialCursor = args1 === null || args1 === void 0 ? void 0 : args1.initialCursor) !== null && _args1$initialCursor !== void 0 ? _args1$initialCursor : null
			}));
		}
		return promise;
	});
	function HydrateClient(props) {
		const dehydratedState = (0, _tanstack_react_query.dehydrate)(getQueryClient());
		return /* @__PURE__ */ react.createElement(_tanstack_react_query.HydrationBoundary, { state: dehydratedState }, props.children);
	}
	return {
		/***
		* Wrapped caller with prefetch helpers
		* Can be used as a regular [server-side caller](https://trpc.io/docs/server/server-side-calls)
		* or using prefetch helpers to put the promise into the QueryClient cache
		* @example
		* ```ts
		* const data = await trpc.post.get("postId");
		*
		* // or
		* void trpc.post.get.prefetch("postId");
		* ```
		*/
		trpc: wrappedProxy,
		/**
		* HoC to hydrate the query client for a client component
		* to pick up the prefetched promise and skip an initial
		* client-side fetch.
		* @example
		* ```tsx
		* // MyRSC.tsx
		* const MyRSC = ({ params }) => {
		*   void trpc.post.get.prefetch(params.postId);
		*
		*   return (
		*     <HydrateClient>
		*       <MyCC postId={params.postId} />
		*     </HydrateClient>
		*    );
		* };
		*
		* // MyCC.tsx
		* "use client"
		* const MyCC = ({ postId }) => {
		*   const { data: post } = trpc.post.get.useQuery(postId);
		*   return <div>{post.title}</div>;
		* };
		* ```
		*/
		HydrateClient
	};
}
//#endregion
exports.createHydrationHelpers = createHydrationHelpers;
