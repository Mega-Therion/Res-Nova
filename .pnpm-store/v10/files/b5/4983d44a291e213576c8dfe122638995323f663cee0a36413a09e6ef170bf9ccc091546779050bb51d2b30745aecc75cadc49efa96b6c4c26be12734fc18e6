const require_getQueryKey = require("./getQueryKey-4D2iXfB-.cjs");
let _trpc_client = require("@trpc/client");
let _tanstack_react_query = require("@tanstack/react-query");
let _trpc_server_unstable_core_do_not_import = require("@trpc/server/unstable-core-do-not-import");
let react = require("react");
react = require_getQueryKey.__toESM(react, 1);
//#region src/shared/proxy/decorationProxy.ts
/**
* Create proxy for decorating procedures
* @internal
*/
function createReactDecoration(hooks) {
	return (0, _trpc_server_unstable_core_do_not_import.createRecursiveProxy)(({ path, args }) => {
		var _rest$;
		const pathCopy = [...path];
		const lastArg = pathCopy.pop();
		if (lastArg === "useMutation") return hooks[lastArg](pathCopy, ...args);
		if (lastArg === "_def") return { path: pathCopy };
		const [input, ...rest] = args;
		const opts = (_rest$ = rest[0]) !== null && _rest$ !== void 0 ? _rest$ : {};
		return hooks[lastArg](pathCopy, input, opts);
	});
}
//#endregion
//#region src/internals/context.tsx
var _React$createContext;
const contextProps = [
	"client",
	"ssrContext",
	"ssrState",
	"abortOnUnmount"
];
const TRPCContext = (_React$createContext = react.createContext) === null || _React$createContext === void 0 ? void 0 : _React$createContext.call(react, null);
//#endregion
//#region src/shared/proxy/utilsProxy.ts
const getQueryType = (utilName) => {
	switch (utilName) {
		case "queryOptions":
		case "fetch":
		case "ensureData":
		case "prefetch":
		case "getData":
		case "setData":
		case "setQueriesData": return "query";
		case "infiniteQueryOptions":
		case "fetchInfinite":
		case "prefetchInfinite":
		case "getInfiniteData":
		case "setInfiniteData": return "infinite";
		case "setMutationDefaults":
		case "getMutationDefaults":
		case "isMutating":
		case "cancel":
		case "invalidate":
		case "refetch":
		case "reset": return "any";
	}
};
/**
* @internal
*/
function createRecursiveUtilsProxy(context) {
	return (0, _trpc_server_unstable_core_do_not_import.createRecursiveProxy)((opts) => {
		const path = [...opts.path];
		const utilName = path.pop();
		const args = [...opts.args];
		const input = args.shift();
		const queryType = getQueryType(utilName);
		const queryKey = require_getQueryKey.getQueryKeyInternal(path, input, queryType);
		return {
			infiniteQueryOptions: () => context.infiniteQueryOptions(path, queryKey, args[0]),
			queryOptions: () => context.queryOptions(path, queryKey, ...args),
			/**
			* DecorateQueryProcedure
			*/
			fetch: () => context.fetchQuery(queryKey, ...args),
			fetchInfinite: () => context.fetchInfiniteQuery(queryKey, args[0]),
			prefetch: () => context.prefetchQuery(queryKey, ...args),
			prefetchInfinite: () => context.prefetchInfiniteQuery(queryKey, args[0]),
			ensureData: () => context.ensureQueryData(queryKey, ...args),
			invalidate: () => context.invalidateQueries(queryKey, ...args),
			reset: () => context.resetQueries(queryKey, ...args),
			refetch: () => context.refetchQueries(queryKey, ...args),
			cancel: () => context.cancelQuery(queryKey, ...args),
			setData: () => {
				context.setQueryData(queryKey, args[0], args[1]);
			},
			setQueriesData: () => context.setQueriesData(queryKey, args[0], args[1], args[2]),
			setInfiniteData: () => {
				context.setInfiniteQueryData(queryKey, args[0], args[1]);
			},
			getData: () => context.getQueryData(queryKey),
			getInfiniteData: () => context.getInfiniteQueryData(queryKey),
			/**
			* DecorateMutationProcedure
			*/
			setMutationDefaults: () => context.setMutationDefaults(require_getQueryKey.getMutationKeyInternal(path), input),
			getMutationDefaults: () => context.getMutationDefaults(require_getQueryKey.getMutationKeyInternal(path)),
			isMutating: () => context.isMutating({ mutationKey: require_getQueryKey.getMutationKeyInternal(path) })
		}[utilName]();
	});
}
/**
* @internal
*/
function createReactQueryUtils(context) {
	const clientProxy = (0, _trpc_client.createTRPCClientProxy)(context.client);
	const proxy = createRecursiveUtilsProxy(context);
	return (0, _trpc_server_unstable_core_do_not_import.createFlatProxy)((key) => {
		const contextName = key;
		if (contextName === "client") return clientProxy;
		if (contextProps.includes(contextName)) return context[contextName];
		return proxy[key];
	});
}
/**
* @internal
*/
function createQueryUtilsProxy(context) {
	return createRecursiveUtilsProxy(context);
}
//#endregion
//#region src/shared/proxy/useQueriesProxy.ts
/**
* Create proxy for `useQueries` options
* @internal
*/
function createUseQueries(client) {
	const untypedClient = client instanceof _trpc_client.TRPCUntypedClient ? client : (0, _trpc_client.getUntypedClient)(client);
	return (0, _trpc_server_unstable_core_do_not_import.createRecursiveProxy)((opts) => {
		const arrayPath = opts.path;
		const dotPath = arrayPath.join(".");
		const [input, _opts] = opts.args;
		return require_getQueryKey._objectSpread2({
			queryKey: require_getQueryKey.getQueryKeyInternal(arrayPath, input, "query"),
			queryFn: () => {
				return untypedClient.query(dotPath, input, _opts === null || _opts === void 0 ? void 0 : _opts.trpc);
			}
		}, _opts);
	});
}
//#endregion
//#region src/internals/getClientArgs.ts
/**
* @internal
*/
function getClientArgs(queryKey, opts, infiniteParams) {
	var _queryKey$;
	const path = queryKey[0];
	let input = (_queryKey$ = queryKey[1]) === null || _queryKey$ === void 0 ? void 0 : _queryKey$.input;
	if (infiniteParams) {
		var _input;
		input = require_getQueryKey._objectSpread2(require_getQueryKey._objectSpread2(require_getQueryKey._objectSpread2({}, (_input = input) !== null && _input !== void 0 ? _input : {}), infiniteParams.pageParam ? { cursor: infiniteParams.pageParam } : {}), {}, { direction: infiniteParams.direction });
	}
	return [
		path.join("."),
		input,
		opts === null || opts === void 0 ? void 0 : opts.trpc
	];
}
//#endregion
//#region \0@oxc-project+runtime@0.149.0/helpers/esm/asyncIterator.js
function _asyncIterator(r) {
	var n, t, o, e = 2;
	for ("undefined" != typeof Symbol && (t = Symbol.asyncIterator, o = Symbol.iterator); e--;) {
		if (t && null != (n = r[t])) return n.call(r);
		if (o && null != (n = r[o])) return new AsyncFromSyncIterator(n.call(r));
		t = "@@asyncIterator", o = "@@iterator";
	}
	throw new TypeError("Object is not async iterable");
}
function AsyncFromSyncIterator(r) {
	function AsyncFromSyncIteratorContinuation(r) {
		if (Object(r) !== r) return Promise.reject(/* @__PURE__ */ new TypeError(r + " is not an object."));
		var n = r.done;
		return Promise.resolve(r.value).then(function(r) {
			return {
				value: r,
				done: n
			};
		});
	}
	return AsyncFromSyncIterator = function AsyncFromSyncIterator(r) {
		this.s = r, this.n = r.next;
	}, AsyncFromSyncIterator.prototype = {
		s: null,
		n: null,
		next: function next() {
			return AsyncFromSyncIteratorContinuation(this.n.apply(this.s, arguments));
		},
		"return": function _return(r) {
			var n = this.s["return"];
			return void 0 === n ? Promise.resolve({
				value: r,
				done: !0
			}) : AsyncFromSyncIteratorContinuation(n.apply(this.s, arguments));
		},
		"throw": function _throw(r) {
			var n = this.s["return"];
			return void 0 === n ? Promise.reject(r) : AsyncFromSyncIteratorContinuation(n.apply(this.s, arguments));
		}
	}, new AsyncFromSyncIterator(r);
}
//#endregion
//#region src/internals/trpcResult.ts
function createTRPCOptionsResult(value) {
	return { path: value.path.join(".") };
}
/**
* Makes a stable reference of the `trpc` prop
*/
function useHookResult(value) {
	const result = createTRPCOptionsResult(value);
	return react.useMemo(() => result, [result]);
}
/**
* @internal
*/
async function buildQueryFromAsyncIterable(asyncIterable, queryClient, queryKey) {
	const query = queryClient.getQueryCache().build(queryClient, { queryKey });
	query.setState({
		data: [],
		status: "success"
	});
	const aggregate = [];
	var _iteratorAbruptCompletion = false;
	var _didIteratorError = false;
	var _iteratorError;
	try {
		for (var _iterator = _asyncIterator(asyncIterable), _step; _iteratorAbruptCompletion = !(_step = await _iterator.next()).done; _iteratorAbruptCompletion = false) {
			const value = _step.value;
			aggregate.push(value);
			query.setState({ data: [...aggregate] });
		}
	} catch (err) {
		_didIteratorError = true;
		_iteratorError = err;
	} finally {
		try {
			if (_iteratorAbruptCompletion && _iterator.return != null) await _iterator.return();
		} finally {
			if (_didIteratorError) throw _iteratorError;
		}
	}
	return aggregate;
}
//#endregion
//#region src/utils/createUtilityFunctions.ts
/**
* Creates a set of utility functions that can be used to interact with `react-query`
* @param opts the `TRPCClient` and `QueryClient` to use
* @returns a set of utility functions that can be used to interact with `react-query`
* @internal
*/
function createUtilityFunctions(opts) {
	const { client, queryClient } = opts;
	const untypedClient = client instanceof _trpc_client.TRPCUntypedClient ? client : (0, _trpc_client.getUntypedClient)(client);
	return {
		infiniteQueryOptions: (path, queryKey, opts) => {
			var _queryKey$, _ref;
			const inputIsSkipToken = ((_queryKey$ = queryKey[1]) === null || _queryKey$ === void 0 ? void 0 : _queryKey$.input) === _tanstack_react_query.skipToken;
			const queryFn = async (queryFnContext) => {
				var _opts$trpc;
				const actualOpts = require_getQueryKey._objectSpread2(require_getQueryKey._objectSpread2({}, opts), {}, { trpc: require_getQueryKey._objectSpread2(require_getQueryKey._objectSpread2({}, opts === null || opts === void 0 ? void 0 : opts.trpc), (opts === null || opts === void 0 || (_opts$trpc = opts.trpc) === null || _opts$trpc === void 0 ? void 0 : _opts$trpc.abortOnUnmount) ? { signal: queryFnContext.signal } : { signal: null }) });
				return await untypedClient.query(...getClientArgs(queryKey, actualOpts, {
					direction: queryFnContext.direction,
					pageParam: queryFnContext.pageParam
				}));
			};
			return Object.assign((0, _tanstack_react_query.infiniteQueryOptions)(require_getQueryKey._objectSpread2(require_getQueryKey._objectSpread2({}, opts), {}, {
				initialData: opts === null || opts === void 0 ? void 0 : opts.initialData,
				queryKey,
				queryFn: inputIsSkipToken ? _tanstack_react_query.skipToken : queryFn,
				initialPageParam: (_ref = opts === null || opts === void 0 ? void 0 : opts.initialCursor) !== null && _ref !== void 0 ? _ref : null
			})), { trpc: createTRPCOptionsResult({ path }) });
		},
		queryOptions: (path, queryKey, opts) => {
			var _queryKey$2;
			const inputIsSkipToken = ((_queryKey$2 = queryKey[1]) === null || _queryKey$2 === void 0 ? void 0 : _queryKey$2.input) === _tanstack_react_query.skipToken;
			const queryFn = async (queryFnContext) => {
				var _opts$trpc2;
				const actualOpts = require_getQueryKey._objectSpread2(require_getQueryKey._objectSpread2({}, opts), {}, { trpc: require_getQueryKey._objectSpread2(require_getQueryKey._objectSpread2({}, opts === null || opts === void 0 ? void 0 : opts.trpc), (opts === null || opts === void 0 || (_opts$trpc2 = opts.trpc) === null || _opts$trpc2 === void 0 ? void 0 : _opts$trpc2.abortOnUnmount) ? { signal: queryFnContext.signal } : { signal: null }) });
				const result = await untypedClient.query(...getClientArgs(queryKey, actualOpts));
				if ((0, _trpc_server_unstable_core_do_not_import.isAsyncIterable)(result)) return buildQueryFromAsyncIterable(result, queryClient, queryKey);
				return result;
			};
			return Object.assign((0, _tanstack_react_query.queryOptions)(require_getQueryKey._objectSpread2(require_getQueryKey._objectSpread2({}, opts), {}, {
				initialData: opts === null || opts === void 0 ? void 0 : opts.initialData,
				queryKey,
				queryFn: inputIsSkipToken ? _tanstack_react_query.skipToken : queryFn
			})), { trpc: createTRPCOptionsResult({ path }) });
		},
		fetchQuery: (queryKey, opts) => {
			return queryClient.fetchQuery(require_getQueryKey._objectSpread2(require_getQueryKey._objectSpread2({}, opts), {}, {
				queryKey,
				queryFn: () => untypedClient.query(...getClientArgs(queryKey, opts))
			}));
		},
		fetchInfiniteQuery: (queryKey, opts) => {
			var _opts$initialCursor;
			return queryClient.fetchInfiniteQuery(require_getQueryKey._objectSpread2(require_getQueryKey._objectSpread2({}, opts), {}, {
				queryKey,
				queryFn: ({ pageParam, direction }) => {
					return untypedClient.query(...getClientArgs(queryKey, opts, {
						pageParam,
						direction
					}));
				},
				initialPageParam: (_opts$initialCursor = opts === null || opts === void 0 ? void 0 : opts.initialCursor) !== null && _opts$initialCursor !== void 0 ? _opts$initialCursor : null
			}));
		},
		prefetchQuery: (queryKey, opts) => {
			return queryClient.prefetchQuery(require_getQueryKey._objectSpread2(require_getQueryKey._objectSpread2({}, opts), {}, {
				queryKey,
				queryFn: () => untypedClient.query(...getClientArgs(queryKey, opts))
			}));
		},
		prefetchInfiniteQuery: (queryKey, opts) => {
			var _opts$initialCursor2;
			return queryClient.prefetchInfiniteQuery(require_getQueryKey._objectSpread2(require_getQueryKey._objectSpread2({}, opts), {}, {
				queryKey,
				queryFn: ({ pageParam, direction }) => {
					return untypedClient.query(...getClientArgs(queryKey, opts, {
						pageParam,
						direction
					}));
				},
				initialPageParam: (_opts$initialCursor2 = opts === null || opts === void 0 ? void 0 : opts.initialCursor) !== null && _opts$initialCursor2 !== void 0 ? _opts$initialCursor2 : null
			}));
		},
		ensureQueryData: (queryKey, opts) => {
			return queryClient.ensureQueryData(require_getQueryKey._objectSpread2(require_getQueryKey._objectSpread2({}, opts), {}, {
				queryKey,
				queryFn: () => untypedClient.query(...getClientArgs(queryKey, opts))
			}));
		},
		invalidateQueries: (queryKey, filters, options) => {
			return queryClient.invalidateQueries(require_getQueryKey._objectSpread2(require_getQueryKey._objectSpread2({}, filters), {}, { queryKey }), options);
		},
		resetQueries: (queryKey, filters, options) => {
			return queryClient.resetQueries(require_getQueryKey._objectSpread2(require_getQueryKey._objectSpread2({}, filters), {}, { queryKey }), options);
		},
		refetchQueries: (queryKey, filters, options) => {
			return queryClient.refetchQueries(require_getQueryKey._objectSpread2(require_getQueryKey._objectSpread2({}, filters), {}, { queryKey }), options);
		},
		cancelQuery: (queryKey, options) => {
			return queryClient.cancelQueries({ queryKey }, options);
		},
		setQueryData: (queryKey, updater, options) => {
			return queryClient.setQueryData(queryKey, updater, options);
		},
		setQueriesData: (queryKey, filters, updater, options) => {
			return queryClient.setQueriesData(require_getQueryKey._objectSpread2(require_getQueryKey._objectSpread2({}, filters), {}, { queryKey }), updater, options);
		},
		getQueryData: (queryKey) => {
			return queryClient.getQueryData(queryKey);
		},
		setInfiniteQueryData: (queryKey, updater, options) => {
			return queryClient.setQueryData(queryKey, updater, options);
		},
		getInfiniteQueryData: (queryKey) => {
			return queryClient.getQueryData(queryKey);
		},
		setMutationDefaults: (mutationKey, options) => {
			const path = mutationKey[0];
			const canonicalMutationFn = (input) => {
				return untypedClient.mutation(...getClientArgs([path, { input }], opts));
			};
			return queryClient.setMutationDefaults(mutationKey, typeof options === "function" ? options({ canonicalMutationFn }) : options);
		},
		getMutationDefaults: (mutationKey) => {
			return queryClient.getMutationDefaults(mutationKey);
		},
		isMutating: (filters) => {
			return queryClient.isMutating(require_getQueryKey._objectSpread2(require_getQueryKey._objectSpread2({}, filters), {}, { exact: true }));
		}
	};
}
//#endregion
//#region src/shared/hooks/createHooksInternal.tsx
const trackResult = (result, onTrackResult) => {
	return new Proxy(result, { get(target, prop) {
		onTrackResult(prop);
		return target[prop];
	} });
};
/**
* @internal
*/
function createRootHooks(config) {
	var _config$overrides$use, _config$overrides, _config$context;
	const mutationSuccessOverride = (_config$overrides$use = config === null || config === void 0 || (_config$overrides = config.overrides) === null || _config$overrides === void 0 || (_config$overrides = _config$overrides.useMutation) === null || _config$overrides === void 0 ? void 0 : _config$overrides.onSuccess) !== null && _config$overrides$use !== void 0 ? _config$overrides$use : ((options) => options.originalFn());
	const Context = (_config$context = config === null || config === void 0 ? void 0 : config.context) !== null && _config$context !== void 0 ? _config$context : TRPCContext;
	const createClient = _trpc_client.createTRPCClient;
	const TRPCProvider = (props) => {
		var _props$ssrState;
		const { abortOnUnmount = false, queryClient, ssrContext } = props;
		const [ssrState, setSSRState] = react.useState((_props$ssrState = props.ssrState) !== null && _props$ssrState !== void 0 ? _props$ssrState : false);
		const client = props.client instanceof _trpc_client.TRPCUntypedClient ? props.client : (0, _trpc_client.getUntypedClient)(props.client);
		const fns = react.useMemo(() => createUtilityFunctions({
			client,
			queryClient
		}), [client, queryClient]);
		const contextValue = react.useMemo(() => require_getQueryKey._objectSpread2({
			abortOnUnmount,
			queryClient,
			client,
			ssrContext: ssrContext !== null && ssrContext !== void 0 ? ssrContext : null,
			ssrState
		}, fns), [
			abortOnUnmount,
			client,
			fns,
			queryClient,
			ssrContext,
			ssrState
		]);
		react.useEffect(() => {
			setSSRState((state) => state ? "mounted" : false);
		}, []);
		return /* @__PURE__ */ react.createElement(Context.Provider, { value: contextValue }, props.children);
	};
	function useContext() {
		const context = react.useContext(Context);
		if (!context) throw new Error("Unable to find tRPC Context. Did you forget to wrap your App inside `withTRPC` HoC?");
		return context;
	}
	/**
	* Hack to make sure errors return `status`='error` when doing SSR
	* @see https://github.com/trpc/trpc/pull/1645
	*/
	function useSSRQueryOptionsIfNeeded(queryKey, opts) {
		var _queryClient$getQuery;
		const { queryClient, ssrState } = useContext();
		return ssrState && ssrState !== "mounted" && ((_queryClient$getQuery = queryClient.getQueryCache().find({ queryKey })) === null || _queryClient$getQuery === void 0 ? void 0 : _queryClient$getQuery.state.status) === "error" ? require_getQueryKey._objectSpread2({ retryOnMount: false }, opts) : opts;
	}
	function useQuery(path, input, opts) {
		var _opts$trpc, _opts$enabled, _ref, _opts$trpc$abortOnUnm, _opts$trpc2;
		const { abortOnUnmount, client, ssrState, queryClient, prefetchQuery } = useContext();
		const queryKey = require_getQueryKey.getQueryKeyInternal(path, input, "query");
		const defaultOpts = queryClient.getQueryDefaults(queryKey);
		const isInputSkipToken = input === _tanstack_react_query.skipToken;
		if (typeof window === "undefined" && ssrState === "prepass" && (opts === null || opts === void 0 || (_opts$trpc = opts.trpc) === null || _opts$trpc === void 0 ? void 0 : _opts$trpc.ssr) !== false && ((_opts$enabled = opts === null || opts === void 0 ? void 0 : opts.enabled) !== null && _opts$enabled !== void 0 ? _opts$enabled : defaultOpts === null || defaultOpts === void 0 ? void 0 : defaultOpts.enabled) !== false && !isInputSkipToken && !queryClient.getQueryCache().find({ queryKey })) prefetchQuery(queryKey, opts);
		const ssrOpts = useSSRQueryOptionsIfNeeded(queryKey, require_getQueryKey._objectSpread2(require_getQueryKey._objectSpread2({}, defaultOpts), opts));
		const shouldAbortOnUnmount = (_ref = (_opts$trpc$abortOnUnm = opts === null || opts === void 0 || (_opts$trpc2 = opts.trpc) === null || _opts$trpc2 === void 0 ? void 0 : _opts$trpc2.abortOnUnmount) !== null && _opts$trpc$abortOnUnm !== void 0 ? _opts$trpc$abortOnUnm : config === null || config === void 0 ? void 0 : config.abortOnUnmount) !== null && _ref !== void 0 ? _ref : abortOnUnmount;
		const hook = (0, _tanstack_react_query.useQuery)(require_getQueryKey._objectSpread2(require_getQueryKey._objectSpread2({}, ssrOpts), {}, {
			queryKey,
			queryFn: isInputSkipToken ? input : async (queryFunctionContext) => {
				const actualOpts = require_getQueryKey._objectSpread2(require_getQueryKey._objectSpread2({}, ssrOpts), {}, { trpc: require_getQueryKey._objectSpread2(require_getQueryKey._objectSpread2({}, ssrOpts === null || ssrOpts === void 0 ? void 0 : ssrOpts.trpc), shouldAbortOnUnmount ? { signal: queryFunctionContext.signal } : { signal: null }) });
				const result = await client.query(...getClientArgs(queryKey, actualOpts));
				if ((0, _trpc_server_unstable_core_do_not_import.isAsyncIterable)(result)) return buildQueryFromAsyncIterable(result, queryClient, queryKey);
				return result;
			}
		}), queryClient);
		hook.trpc = useHookResult({ path });
		return hook;
	}
	function usePrefetchQuery(path, input, opts) {
		var _ref2, _opts$trpc$abortOnUnm2, _opts$trpc3;
		const context = useContext();
		const queryKey = require_getQueryKey.getQueryKeyInternal(path, input, "query");
		const isInputSkipToken = input === _tanstack_react_query.skipToken;
		const shouldAbortOnUnmount = (_ref2 = (_opts$trpc$abortOnUnm2 = opts === null || opts === void 0 || (_opts$trpc3 = opts.trpc) === null || _opts$trpc3 === void 0 ? void 0 : _opts$trpc3.abortOnUnmount) !== null && _opts$trpc$abortOnUnm2 !== void 0 ? _opts$trpc$abortOnUnm2 : config === null || config === void 0 ? void 0 : config.abortOnUnmount) !== null && _ref2 !== void 0 ? _ref2 : context.abortOnUnmount;
		(0, _tanstack_react_query.usePrefetchQuery)(require_getQueryKey._objectSpread2(require_getQueryKey._objectSpread2({}, opts), {}, {
			queryKey,
			queryFn: isInputSkipToken ? input : (queryFunctionContext) => {
				const actualOpts = { trpc: require_getQueryKey._objectSpread2(require_getQueryKey._objectSpread2({}, opts === null || opts === void 0 ? void 0 : opts.trpc), shouldAbortOnUnmount ? { signal: queryFunctionContext.signal } : {}) };
				return context.client.query(...getClientArgs(queryKey, actualOpts));
			}
		}));
	}
	function useSuspenseQuery(path, input, opts) {
		var _ref3, _opts$trpc$abortOnUnm3, _opts$trpc4;
		const context = useContext();
		const queryKey = require_getQueryKey.getQueryKeyInternal(path, input, "query");
		const shouldAbortOnUnmount = (_ref3 = (_opts$trpc$abortOnUnm3 = opts === null || opts === void 0 || (_opts$trpc4 = opts.trpc) === null || _opts$trpc4 === void 0 ? void 0 : _opts$trpc4.abortOnUnmount) !== null && _opts$trpc$abortOnUnm3 !== void 0 ? _opts$trpc$abortOnUnm3 : config === null || config === void 0 ? void 0 : config.abortOnUnmount) !== null && _ref3 !== void 0 ? _ref3 : context.abortOnUnmount;
		const hook = (0, _tanstack_react_query.useSuspenseQuery)(require_getQueryKey._objectSpread2(require_getQueryKey._objectSpread2({}, opts), {}, {
			queryKey,
			queryFn: (queryFunctionContext) => {
				const actualOpts = require_getQueryKey._objectSpread2(require_getQueryKey._objectSpread2({}, opts), {}, { trpc: require_getQueryKey._objectSpread2(require_getQueryKey._objectSpread2({}, opts === null || opts === void 0 ? void 0 : opts.trpc), shouldAbortOnUnmount ? { signal: queryFunctionContext.signal } : { signal: null }) });
				return context.client.query(...getClientArgs(queryKey, actualOpts));
			}
		}), context.queryClient);
		hook.trpc = useHookResult({ path });
		return [hook.data, hook];
	}
	function useMutation(path, opts) {
		const { client, queryClient } = useContext();
		const mutationKey = require_getQueryKey.getMutationKeyInternal(path);
		const defaultOpts = queryClient.defaultMutationOptions(queryClient.getMutationDefaults(mutationKey));
		const hook = (0, _tanstack_react_query.useMutation)(require_getQueryKey._objectSpread2(require_getQueryKey._objectSpread2({}, opts), {}, {
			mutationKey,
			mutationFn: (input) => {
				return client.mutation(...getClientArgs([path, { input }], opts));
			},
			onSuccess(...args) {
				var _ref4, _opts$meta;
				const originalFn = () => {
					var _opts$onSuccess, _opts$onSuccess2, _defaultOpts$onSucces;
					return (_opts$onSuccess = opts === null || opts === void 0 || (_opts$onSuccess2 = opts.onSuccess) === null || _opts$onSuccess2 === void 0 ? void 0 : _opts$onSuccess2.call(opts, ...args)) !== null && _opts$onSuccess !== void 0 ? _opts$onSuccess : defaultOpts === null || defaultOpts === void 0 || (_defaultOpts$onSucces = defaultOpts.onSuccess) === null || _defaultOpts$onSucces === void 0 ? void 0 : _defaultOpts$onSucces.call(defaultOpts, ...args);
				};
				return mutationSuccessOverride({
					originalFn,
					queryClient,
					meta: (_ref4 = (_opts$meta = opts === null || opts === void 0 ? void 0 : opts.meta) !== null && _opts$meta !== void 0 ? _opts$meta : defaultOpts === null || defaultOpts === void 0 ? void 0 : defaultOpts.meta) !== null && _ref4 !== void 0 ? _ref4 : {}
				});
			}
		}), queryClient);
		hook.trpc = useHookResult({ path });
		return hook;
	}
	const initialStateIdle = {
		data: void 0,
		error: null,
		status: "idle"
	};
	const initialStateConnecting = {
		data: void 0,
		error: null,
		status: "connecting"
	};
	/* istanbul ignore next -- @preserve */
	function useSubscription(path, input, opts) {
		var _opts$enabled2;
		const enabled = (_opts$enabled2 = opts === null || opts === void 0 ? void 0 : opts.enabled) !== null && _opts$enabled2 !== void 0 ? _opts$enabled2 : input !== _tanstack_react_query.skipToken;
		const queryKey = (0, _tanstack_react_query.hashKey)(require_getQueryKey.getQueryKeyInternal(path, input, "any"));
		const { client } = useContext();
		const optsRef = react.useRef(opts);
		react.useEffect(() => {
			optsRef.current = opts;
		});
		const [trackedProps] = react.useState(/* @__PURE__ */ new Set([]));
		const addTrackedProp = react.useCallback((key) => {
			trackedProps.add(key);
		}, [trackedProps]);
		const currentSubscriptionRef = react.useRef(null);
		const updateState = react.useCallback((callback) => {
			const prev = resultRef.current;
			const next = resultRef.current = callback(prev);
			let shouldUpdate = false;
			for (const key of trackedProps) if (prev[key] !== next[key]) {
				shouldUpdate = true;
				break;
			}
			if (shouldUpdate) setState(trackResult(next, addTrackedProp));
		}, [addTrackedProp, trackedProps]);
		const reset = react.useCallback(() => {
			var _currentSubscriptionR;
			(_currentSubscriptionR = currentSubscriptionRef.current) === null || _currentSubscriptionR === void 0 || _currentSubscriptionR.unsubscribe();
			if (!enabled) {
				updateState(() => require_getQueryKey._objectSpread2(require_getQueryKey._objectSpread2({}, initialStateIdle), {}, { reset }));
				return;
			}
			updateState(() => require_getQueryKey._objectSpread2(require_getQueryKey._objectSpread2({}, initialStateConnecting), {}, { reset }));
			const subscription = client.subscription(path.join("."), input !== null && input !== void 0 ? input : void 0, {
				onStarted: () => {
					var _optsRef$current$onSt, _optsRef$current;
					(_optsRef$current$onSt = (_optsRef$current = optsRef.current).onStarted) === null || _optsRef$current$onSt === void 0 || _optsRef$current$onSt.call(_optsRef$current);
					updateState((prev) => require_getQueryKey._objectSpread2(require_getQueryKey._objectSpread2({}, prev), {}, {
						status: "pending",
						error: null
					}));
				},
				onData: (data) => {
					var _optsRef$current$onDa, _optsRef$current2;
					(_optsRef$current$onDa = (_optsRef$current2 = optsRef.current).onData) === null || _optsRef$current$onDa === void 0 || _optsRef$current$onDa.call(_optsRef$current2, data);
					updateState((prev) => require_getQueryKey._objectSpread2(require_getQueryKey._objectSpread2({}, prev), {}, {
						status: "pending",
						data,
						error: null
					}));
				},
				onError: (error) => {
					var _optsRef$current$onEr, _optsRef$current3;
					(_optsRef$current$onEr = (_optsRef$current3 = optsRef.current).onError) === null || _optsRef$current$onEr === void 0 || _optsRef$current$onEr.call(_optsRef$current3, error);
					updateState((prev) => require_getQueryKey._objectSpread2(require_getQueryKey._objectSpread2({}, prev), {}, {
						status: "error",
						error
					}));
				},
				onConnectionStateChange: (result) => {
					updateState((prev) => {
						switch (result.state) {
							case "idle": return require_getQueryKey._objectSpread2(require_getQueryKey._objectSpread2({}, prev), {}, {
								status: result.state,
								error: null,
								data: void 0
							});
							case "connecting": return require_getQueryKey._objectSpread2(require_getQueryKey._objectSpread2({}, prev), {}, {
								error: result.error,
								status: result.state
							});
							case "pending": return prev;
						}
					});
				},
				onComplete: () => {
					var _optsRef$current$onCo, _optsRef$current4;
					(_optsRef$current$onCo = (_optsRef$current4 = optsRef.current).onComplete) === null || _optsRef$current$onCo === void 0 || _optsRef$current$onCo.call(_optsRef$current4);
					updateState((prev) => require_getQueryKey._objectSpread2(require_getQueryKey._objectSpread2({}, prev), {}, {
						status: "idle",
						error: null,
						data: void 0
					}));
				}
			});
			currentSubscriptionRef.current = subscription;
		}, [
			client,
			queryKey,
			enabled,
			updateState
		]);
		react.useEffect(() => {
			reset();
			return () => {
				var _currentSubscriptionR2;
				(_currentSubscriptionR2 = currentSubscriptionRef.current) === null || _currentSubscriptionR2 === void 0 || _currentSubscriptionR2.unsubscribe();
			};
		}, [reset]);
		const resultRef = react.useRef(enabled ? require_getQueryKey._objectSpread2(require_getQueryKey._objectSpread2({}, initialStateConnecting), {}, { reset }) : require_getQueryKey._objectSpread2(require_getQueryKey._objectSpread2({}, initialStateIdle), {}, { reset }));
		const [state, setState] = react.useState(trackResult(resultRef.current, addTrackedProp));
		return state;
	}
	function useInfiniteQuery(path, input, opts) {
		var _opts$trpc5, _opts$enabled3, _opts$trpc$abortOnUnm4, _opts$trpc6, _opts$initialCursor;
		const { client, ssrState, prefetchInfiniteQuery, queryClient, abortOnUnmount } = useContext();
		const queryKey = require_getQueryKey.getQueryKeyInternal(path, input, "infinite");
		const defaultOpts = queryClient.getQueryDefaults(queryKey);
		const isInputSkipToken = input === _tanstack_react_query.skipToken;
		if (typeof window === "undefined" && ssrState === "prepass" && (opts === null || opts === void 0 || (_opts$trpc5 = opts.trpc) === null || _opts$trpc5 === void 0 ? void 0 : _opts$trpc5.ssr) !== false && ((_opts$enabled3 = opts === null || opts === void 0 ? void 0 : opts.enabled) !== null && _opts$enabled3 !== void 0 ? _opts$enabled3 : defaultOpts === null || defaultOpts === void 0 ? void 0 : defaultOpts.enabled) !== false && !isInputSkipToken && !queryClient.getQueryCache().find({ queryKey })) prefetchInfiniteQuery(queryKey, require_getQueryKey._objectSpread2(require_getQueryKey._objectSpread2({}, defaultOpts), opts));
		const ssrOpts = useSSRQueryOptionsIfNeeded(queryKey, require_getQueryKey._objectSpread2(require_getQueryKey._objectSpread2({}, defaultOpts), opts));
		const shouldAbortOnUnmount = (_opts$trpc$abortOnUnm4 = opts === null || opts === void 0 || (_opts$trpc6 = opts.trpc) === null || _opts$trpc6 === void 0 ? void 0 : _opts$trpc6.abortOnUnmount) !== null && _opts$trpc$abortOnUnm4 !== void 0 ? _opts$trpc$abortOnUnm4 : abortOnUnmount;
		const hook = (0, _tanstack_react_query.useInfiniteQuery)(require_getQueryKey._objectSpread2(require_getQueryKey._objectSpread2({}, ssrOpts), {}, {
			initialPageParam: (_opts$initialCursor = opts.initialCursor) !== null && _opts$initialCursor !== void 0 ? _opts$initialCursor : null,
			persister: opts.persister,
			queryKey,
			queryFn: isInputSkipToken ? input : (queryFunctionContext) => {
				var _queryFunctionContext;
				const actualOpts = require_getQueryKey._objectSpread2(require_getQueryKey._objectSpread2({}, ssrOpts), {}, { trpc: require_getQueryKey._objectSpread2(require_getQueryKey._objectSpread2({}, ssrOpts === null || ssrOpts === void 0 ? void 0 : ssrOpts.trpc), shouldAbortOnUnmount ? { signal: queryFunctionContext.signal } : { signal: null }) });
				return client.query(...getClientArgs(queryKey, actualOpts, {
					pageParam: (_queryFunctionContext = queryFunctionContext.pageParam) !== null && _queryFunctionContext !== void 0 ? _queryFunctionContext : opts.initialCursor,
					direction: queryFunctionContext.direction
				}));
			}
		}), queryClient);
		hook.trpc = useHookResult({ path });
		return hook;
	}
	function usePrefetchInfiniteQuery(path, input, opts) {
		var _opts$trpc$abortOnUnm5, _opts$trpc7, _opts$initialCursor2;
		const context = useContext();
		const queryKey = require_getQueryKey.getQueryKeyInternal(path, input, "infinite");
		const defaultOpts = context.queryClient.getQueryDefaults(queryKey);
		const isInputSkipToken = input === _tanstack_react_query.skipToken;
		const ssrOpts = useSSRQueryOptionsIfNeeded(queryKey, require_getQueryKey._objectSpread2(require_getQueryKey._objectSpread2({}, defaultOpts), opts));
		const shouldAbortOnUnmount = (_opts$trpc$abortOnUnm5 = opts === null || opts === void 0 || (_opts$trpc7 = opts.trpc) === null || _opts$trpc7 === void 0 ? void 0 : _opts$trpc7.abortOnUnmount) !== null && _opts$trpc$abortOnUnm5 !== void 0 ? _opts$trpc$abortOnUnm5 : context.abortOnUnmount;
		(0, _tanstack_react_query.usePrefetchInfiniteQuery)(require_getQueryKey._objectSpread2(require_getQueryKey._objectSpread2({}, opts), {}, {
			initialPageParam: (_opts$initialCursor2 = opts.initialCursor) !== null && _opts$initialCursor2 !== void 0 ? _opts$initialCursor2 : null,
			queryKey,
			queryFn: isInputSkipToken ? input : (queryFunctionContext) => {
				var _queryFunctionContext2;
				const actualOpts = require_getQueryKey._objectSpread2(require_getQueryKey._objectSpread2({}, ssrOpts), {}, { trpc: require_getQueryKey._objectSpread2(require_getQueryKey._objectSpread2({}, ssrOpts === null || ssrOpts === void 0 ? void 0 : ssrOpts.trpc), shouldAbortOnUnmount ? { signal: queryFunctionContext.signal } : {}) });
				return context.client.query(...getClientArgs(queryKey, actualOpts, {
					pageParam: (_queryFunctionContext2 = queryFunctionContext.pageParam) !== null && _queryFunctionContext2 !== void 0 ? _queryFunctionContext2 : opts.initialCursor,
					direction: queryFunctionContext.direction
				}));
			}
		}));
	}
	function useSuspenseInfiniteQuery(path, input, opts) {
		var _opts$trpc$abortOnUnm6, _opts$trpc8, _opts$initialCursor3;
		const context = useContext();
		const queryKey = require_getQueryKey.getQueryKeyInternal(path, input, "infinite");
		const defaultOpts = context.queryClient.getQueryDefaults(queryKey);
		const ssrOpts = useSSRQueryOptionsIfNeeded(queryKey, require_getQueryKey._objectSpread2(require_getQueryKey._objectSpread2({}, defaultOpts), opts));
		const shouldAbortOnUnmount = (_opts$trpc$abortOnUnm6 = opts === null || opts === void 0 || (_opts$trpc8 = opts.trpc) === null || _opts$trpc8 === void 0 ? void 0 : _opts$trpc8.abortOnUnmount) !== null && _opts$trpc$abortOnUnm6 !== void 0 ? _opts$trpc$abortOnUnm6 : context.abortOnUnmount;
		const hook = (0, _tanstack_react_query.useSuspenseInfiniteQuery)(require_getQueryKey._objectSpread2(require_getQueryKey._objectSpread2({}, opts), {}, {
			initialPageParam: (_opts$initialCursor3 = opts.initialCursor) !== null && _opts$initialCursor3 !== void 0 ? _opts$initialCursor3 : null,
			queryKey,
			queryFn: (queryFunctionContext) => {
				var _queryFunctionContext3;
				const actualOpts = require_getQueryKey._objectSpread2(require_getQueryKey._objectSpread2({}, ssrOpts), {}, { trpc: require_getQueryKey._objectSpread2(require_getQueryKey._objectSpread2({}, ssrOpts === null || ssrOpts === void 0 ? void 0 : ssrOpts.trpc), shouldAbortOnUnmount ? { signal: queryFunctionContext.signal } : {}) });
				return context.client.query(...getClientArgs(queryKey, actualOpts, {
					pageParam: (_queryFunctionContext3 = queryFunctionContext.pageParam) !== null && _queryFunctionContext3 !== void 0 ? _queryFunctionContext3 : opts.initialCursor,
					direction: queryFunctionContext.direction
				}));
			}
		}), context.queryClient);
		hook.trpc = useHookResult({ path });
		return [hook.data, hook];
	}
	const useQueries = (queriesCallback, options) => {
		const { ssrState, queryClient, prefetchQuery, client } = useContext();
		const queries = queriesCallback(createUseQueries(client));
		if (typeof window === "undefined" && ssrState === "prepass") for (const query of queries) {
			var _queryOption$trpc;
			const queryOption = query;
			if (((_queryOption$trpc = queryOption.trpc) === null || _queryOption$trpc === void 0 ? void 0 : _queryOption$trpc.ssr) !== false && !queryClient.getQueryCache().find({ queryKey: queryOption.queryKey })) prefetchQuery(queryOption.queryKey, queryOption);
		}
		return (0, _tanstack_react_query.useQueries)({
			queries: queries.map((query) => require_getQueryKey._objectSpread2(require_getQueryKey._objectSpread2({}, query), {}, { queryKey: query.queryKey })),
			combine: options === null || options === void 0 ? void 0 : options.combine
		}, queryClient);
	};
	const useSuspenseQueries = (queriesCallback) => {
		const { queryClient, client } = useContext();
		const queries = queriesCallback(createUseQueries(client));
		const hook = (0, _tanstack_react_query.useSuspenseQueries)({ queries: queries.map((query) => require_getQueryKey._objectSpread2(require_getQueryKey._objectSpread2({}, query), {}, {
			queryFn: query.queryFn,
			queryKey: query.queryKey
		})) }, queryClient);
		return [hook.map((h) => h.data), hook];
	};
	return {
		Provider: TRPCProvider,
		createClient,
		useContext,
		useUtils: useContext,
		useQuery,
		usePrefetchQuery,
		useSuspenseQuery,
		useQueries,
		useSuspenseQueries,
		useMutation,
		useSubscription,
		useInfiniteQuery,
		usePrefetchInfiniteQuery,
		useSuspenseInfiniteQuery
	};
}
//#endregion
//#region src/shared/queryClient.ts
/**
* @internal
*/
const getQueryClient = (config) => {
	var _config$queryClient;
	return (_config$queryClient = config.queryClient) !== null && _config$queryClient !== void 0 ? _config$queryClient : new _tanstack_react_query.QueryClient(config.queryClientConfig);
};
//#endregion
Object.defineProperty(exports, "TRPCContext", {
	enumerable: true,
	get: function() {
		return TRPCContext;
	}
});
Object.defineProperty(exports, "contextProps", {
	enumerable: true,
	get: function() {
		return contextProps;
	}
});
Object.defineProperty(exports, "createQueryUtilsProxy", {
	enumerable: true,
	get: function() {
		return createQueryUtilsProxy;
	}
});
Object.defineProperty(exports, "createReactDecoration", {
	enumerable: true,
	get: function() {
		return createReactDecoration;
	}
});
Object.defineProperty(exports, "createReactQueryUtils", {
	enumerable: true,
	get: function() {
		return createReactQueryUtils;
	}
});
Object.defineProperty(exports, "createRootHooks", {
	enumerable: true,
	get: function() {
		return createRootHooks;
	}
});
Object.defineProperty(exports, "createUseQueries", {
	enumerable: true,
	get: function() {
		return createUseQueries;
	}
});
Object.defineProperty(exports, "createUtilityFunctions", {
	enumerable: true,
	get: function() {
		return createUtilityFunctions;
	}
});
Object.defineProperty(exports, "getClientArgs", {
	enumerable: true,
	get: function() {
		return getClientArgs;
	}
});
Object.defineProperty(exports, "getQueryClient", {
	enumerable: true,
	get: function() {
		return getQueryClient;
	}
});
Object.defineProperty(exports, "getQueryType", {
	enumerable: true,
	get: function() {
		return getQueryType;
	}
});
