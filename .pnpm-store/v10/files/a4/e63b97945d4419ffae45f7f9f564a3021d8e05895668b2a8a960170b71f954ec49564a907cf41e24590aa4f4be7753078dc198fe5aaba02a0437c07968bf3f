//#region \0rolldown/runtime.js
var __create = Object.create;
var __defProp = Object.defineProperty;
var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __getProtoOf = Object.getPrototypeOf;
var __hasOwnProp = Object.prototype.hasOwnProperty;
var __copyProps = (to, from, except, desc) => {
	if (from && typeof from === "object" || typeof from === "function") for (var keys = __getOwnPropNames(from), i = 0, n = keys.length, key; i < n; i++) {
		key = keys[i];
		if (!__hasOwnProp.call(to, key) && key !== except) __defProp(to, key, {
			get: ((k) => from[k]).bind(null, key),
			enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable
		});
	}
	return to;
};
var __toESM = (mod, isNodeMode, target) => (target = mod != null ? __create(__getProtoOf(mod)) : {}, __copyProps(isNodeMode || !mod || !mod.__esModule || !__hasOwnProp.call(mod, "default") ? __defProp(target, "default", {
	value: mod,
	enumerable: true
}) : target, mod));
//#endregion
let _tanstack_react_query = require("@tanstack/react-query");
let _trpc_server_unstable_core_do_not_import = require("@trpc/server/unstable-core-do-not-import");
//#region \0@oxc-project+runtime@0.149.0/helpers/esm/objectWithoutPropertiesLoose.js
function _objectWithoutPropertiesLoose(r, e) {
	if (null == r) return {};
	var t = {};
	for (var n in r) if ({}.hasOwnProperty.call(r, n)) {
		if (e.includes(n)) continue;
		t[n] = r[n];
	}
	return t;
}
//#endregion
//#region \0@oxc-project+runtime@0.149.0/helpers/esm/objectWithoutProperties.js
function _objectWithoutProperties(e, t) {
	if (null == e) return {};
	var o, r, i = _objectWithoutPropertiesLoose(e, t);
	if (Object.getOwnPropertySymbols) {
		var s = Object.getOwnPropertySymbols(e);
		for (r = 0; r < s.length; r++) o = s[r], t.includes(o) || {}.propertyIsEnumerable.call(e, o) && (i[o] = e[o]);
	}
	return i;
}
//#endregion
//#region \0@oxc-project+runtime@0.149.0/helpers/esm/typeof.js
function _typeof(o) {
	"@babel/helpers - typeof";
	return _typeof = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function(o) {
		return typeof o;
	} : function(o) {
		return o && "function" == typeof Symbol && o.constructor === Symbol && o !== Symbol.prototype ? "symbol" : typeof o;
	}, _typeof(o);
}
//#endregion
//#region \0@oxc-project+runtime@0.149.0/helpers/esm/toPrimitive.js
function toPrimitive(t, r) {
	if ("object" != _typeof(t) || !t) return t;
	var e = t[Symbol.toPrimitive];
	if (void 0 !== e) {
		var i = e.call(t, r || "default");
		if ("object" != _typeof(i)) return i;
		throw new TypeError("@@toPrimitive must return a primitive value.");
	}
	return ("string" === r ? String : Number)(t);
}
//#endregion
//#region \0@oxc-project+runtime@0.149.0/helpers/esm/toPropertyKey.js
function toPropertyKey(t) {
	var i = toPrimitive(t, "string");
	return "symbol" == _typeof(i) ? i : i + "";
}
//#endregion
//#region \0@oxc-project+runtime@0.149.0/helpers/esm/defineProperty.js
function _defineProperty(e, r, t) {
	return (r = toPropertyKey(r)) in e ? Object.defineProperty(e, r, {
		value: t,
		enumerable: !0,
		configurable: !0,
		writable: !0
	}) : e[r] = t, e;
}
//#endregion
//#region \0@oxc-project+runtime@0.149.0/helpers/esm/objectSpread2.js
function ownKeys(e, r) {
	var t = Object.keys(e);
	if (Object.getOwnPropertySymbols) {
		var o = Object.getOwnPropertySymbols(e);
		r && (o = o.filter(function(r) {
			return Object.getOwnPropertyDescriptor(e, r).enumerable;
		})), t.push.apply(t, o);
	}
	return t;
}
function _objectSpread2(e) {
	for (var r = 1; r < arguments.length; r++) {
		var t = null != arguments[r] ? arguments[r] : {};
		r % 2 ? ownKeys(Object(t), !0).forEach(function(r) {
			_defineProperty(e, r, t[r]);
		}) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object.getOwnPropertyDescriptors(t)) : ownKeys(Object(t)).forEach(function(r) {
			Object.defineProperty(e, r, Object.getOwnPropertyDescriptor(t, r));
		});
	}
	return e;
}
//#endregion
//#region src/internals/getQueryKey.ts
const _excluded = ["cursor", "direction"];
/**
* To allow easy interactions with groups of related queries, such as
* invalidating all queries of a router, we use an array as the path when
* storing in tanstack query.
**/
function getQueryKeyInternal(path, input, type) {
	const splitPath = path.flatMap((part) => part.split("."));
	if (!input && (!type || type === "any")) return splitPath.length ? [splitPath] : [];
	if (type === "infinite" && (0, _trpc_server_unstable_core_do_not_import.isObject)(input) && ("direction" in input || "cursor" in input)) {
		const { cursor: _, direction: __ } = input;
		return [splitPath, {
			input: _objectWithoutProperties(input, _excluded),
			type: "infinite"
		}];
	}
	return [splitPath, _objectSpread2(_objectSpread2({}, typeof input !== "undefined" && input !== _tanstack_react_query.skipToken && { input }), type && type !== "any" && { type })];
}
function getMutationKeyInternal(path) {
	return getQueryKeyInternal(path, void 0, "any");
}
/**
* Method to extract the query key for a procedure
* @param procedureOrRouter - procedure or AnyRouter
* @param input - input to procedureOrRouter
* @param type - defaults to `any`
* @see https://trpc.io/docs/v11/getQueryKey
*/
function getQueryKey(procedureOrRouter, ..._params) {
	const [input, type] = _params;
	const path = procedureOrRouter._def().path;
	return getQueryKeyInternal(path, input, type !== null && type !== void 0 ? type : "any");
}
/**
* Method to extract the mutation key for a procedure
* @param procedure - procedure
* @see https://trpc.io/docs/v11/getQueryKey#mutations
*/
function getMutationKey(procedure) {
	const path = procedure._def().path;
	return getMutationKeyInternal(path);
}
//#endregion
Object.defineProperty(exports, "__toESM", {
	enumerable: true,
	get: function() {
		return __toESM;
	}
});
Object.defineProperty(exports, "_objectSpread2", {
	enumerable: true,
	get: function() {
		return _objectSpread2;
	}
});
Object.defineProperty(exports, "_objectWithoutProperties", {
	enumerable: true,
	get: function() {
		return _objectWithoutProperties;
	}
});
Object.defineProperty(exports, "getMutationKey", {
	enumerable: true,
	get: function() {
		return getMutationKey;
	}
});
Object.defineProperty(exports, "getMutationKeyInternal", {
	enumerable: true,
	get: function() {
		return getMutationKeyInternal;
	}
});
Object.defineProperty(exports, "getQueryKey", {
	enumerable: true,
	get: function() {
		return getQueryKey;
	}
});
Object.defineProperty(exports, "getQueryKeyInternal", {
	enumerable: true,
	get: function() {
		return getQueryKeyInternal;
	}
});
