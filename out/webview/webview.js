function Y_(S) {
  return S && S.__esModule && Object.prototype.hasOwnProperty.call(S, "default") ? S.default : S;
}
var FS = { exports: {} }, uv = {}, HS = { exports: {} }, Ut = {};
/**
 * @license React
 * react.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var RE;
function W_() {
  if (RE)
    return Ut;
  RE = 1;
  var S = Symbol.for("react.element"), w = Symbol.for("react.portal"), b = Symbol.for("react.fragment"), U = Symbol.for("react.strict_mode"), X = Symbol.for("react.profiler"), W = Symbol.for("react.provider"), y = Symbol.for("react.context"), ce = Symbol.for("react.forward_ref"), B = Symbol.for("react.suspense"), K = Symbol.for("react.memo"), ye = Symbol.for("react.lazy"), ne = Symbol.iterator;
  function oe(O) {
    return O === null || typeof O != "object" ? null : (O = ne && O[ne] || O["@@iterator"], typeof O == "function" ? O : null);
  }
  var V = { isMounted: function() {
    return !1;
  }, enqueueForceUpdate: function() {
  }, enqueueReplaceState: function() {
  }, enqueueSetState: function() {
  } }, $ = Object.assign, de = {};
  function Ae(O, q, Re) {
    this.props = O, this.context = q, this.refs = de, this.updater = Re || V;
  }
  Ae.prototype.isReactComponent = {}, Ae.prototype.setState = function(O, q) {
    if (typeof O != "object" && typeof O != "function" && O != null)
      throw Error("setState(...): takes an object of state variables to update or a function which returns an object of state variables.");
    this.updater.enqueueSetState(this, O, q, "setState");
  }, Ae.prototype.forceUpdate = function(O) {
    this.updater.enqueueForceUpdate(this, O, "forceUpdate");
  };
  function Dt() {
  }
  Dt.prototype = Ae.prototype;
  function rt(O, q, Re) {
    this.props = O, this.context = q, this.refs = de, this.updater = Re || V;
  }
  var Ke = rt.prototype = new Dt();
  Ke.constructor = rt, $(Ke, Ae.prototype), Ke.isPureReactComponent = !0;
  var ct = Array.isArray, ke = Object.prototype.hasOwnProperty, at = { current: null }, Ye = { key: !0, ref: !0, __self: !0, __source: !0 };
  function be(O, q, Re) {
    var Me, ft = {}, vt = null, Ge = null;
    if (q != null)
      for (Me in q.ref !== void 0 && (Ge = q.ref), q.key !== void 0 && (vt = "" + q.key), q)
        ke.call(q, Me) && !Ye.hasOwnProperty(Me) && (ft[Me] = q[Me]);
    var St = arguments.length - 2;
    if (St === 1)
      ft.children = Re;
    else if (1 < St) {
      for (var ht = Array(St), Wt = 0; Wt < St; Wt++)
        ht[Wt] = arguments[Wt + 2];
      ft.children = ht;
    }
    if (O && O.defaultProps)
      for (Me in St = O.defaultProps, St)
        ft[Me] === void 0 && (ft[Me] = St[Me]);
    return { $$typeof: S, type: O, key: vt, ref: Ge, props: ft, _owner: at.current };
  }
  function Oe(O, q) {
    return { $$typeof: S, type: O.type, key: q, ref: O.ref, props: O.props, _owner: O._owner };
  }
  function $e(O) {
    return typeof O == "object" && O !== null && O.$$typeof === S;
  }
  function it(O) {
    var q = { "=": "=0", ":": "=2" };
    return "$" + O.replace(/[=:]/g, function(Re) {
      return q[Re];
    });
  }
  var Rt = /\/+/g;
  function Ie(O, q) {
    return typeof O == "object" && O !== null && O.key != null ? it("" + O.key) : q.toString(36);
  }
  function st(O, q, Re, Me, ft) {
    var vt = typeof O;
    (vt === "undefined" || vt === "boolean") && (O = null);
    var Ge = !1;
    if (O === null)
      Ge = !0;
    else
      switch (vt) {
        case "string":
        case "number":
          Ge = !0;
          break;
        case "object":
          switch (O.$$typeof) {
            case S:
            case w:
              Ge = !0;
          }
      }
    if (Ge)
      return Ge = O, ft = ft(Ge), O = Me === "" ? "." + Ie(Ge, 0) : Me, ct(ft) ? (Re = "", O != null && (Re = O.replace(Rt, "$&/") + "/"), st(ft, q, Re, "", function(Wt) {
        return Wt;
      })) : ft != null && ($e(ft) && (ft = Oe(ft, Re + (!ft.key || Ge && Ge.key === ft.key ? "" : ("" + ft.key).replace(Rt, "$&/") + "/") + O)), q.push(ft)), 1;
    if (Ge = 0, Me = Me === "" ? "." : Me + ":", ct(O))
      for (var St = 0; St < O.length; St++) {
        vt = O[St];
        var ht = Me + Ie(vt, St);
        Ge += st(vt, q, Re, ht, ft);
      }
    else if (ht = oe(O), typeof ht == "function")
      for (O = ht.call(O), St = 0; !(vt = O.next()).done; )
        vt = vt.value, ht = Me + Ie(vt, St++), Ge += st(vt, q, Re, ht, ft);
    else if (vt === "object")
      throw q = String(O), Error("Objects are not valid as a React child (found: " + (q === "[object Object]" ? "object with keys {" + Object.keys(O).join(", ") + "}" : q) + "). If you meant to render a collection of children, use an array instead.");
    return Ge;
  }
  function Nt(O, q, Re) {
    if (O == null)
      return O;
    var Me = [], ft = 0;
    return st(O, Me, "", "", function(vt) {
      return q.call(Re, vt, ft++);
    }), Me;
  }
  function yt(O) {
    if (O._status === -1) {
      var q = O._result;
      q = q(), q.then(function(Re) {
        (O._status === 0 || O._status === -1) && (O._status = 1, O._result = Re);
      }, function(Re) {
        (O._status === 0 || O._status === -1) && (O._status = 2, O._result = Re);
      }), O._status === -1 && (O._status = 0, O._result = q);
    }
    if (O._status === 1)
      return O._result.default;
    throw O._result;
  }
  var Se = { current: null }, I = { transition: null }, Ue = { ReactCurrentDispatcher: Se, ReactCurrentBatchConfig: I, ReactCurrentOwner: at };
  function pe() {
    throw Error("act(...) is not supported in production builds of React.");
  }
  return Ut.Children = { map: Nt, forEach: function(O, q, Re) {
    Nt(O, function() {
      q.apply(this, arguments);
    }, Re);
  }, count: function(O) {
    var q = 0;
    return Nt(O, function() {
      q++;
    }), q;
  }, toArray: function(O) {
    return Nt(O, function(q) {
      return q;
    }) || [];
  }, only: function(O) {
    if (!$e(O))
      throw Error("React.Children.only expected to receive a single React element child.");
    return O;
  } }, Ut.Component = Ae, Ut.Fragment = b, Ut.Profiler = X, Ut.PureComponent = rt, Ut.StrictMode = U, Ut.Suspense = B, Ut.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED = Ue, Ut.act = pe, Ut.cloneElement = function(O, q, Re) {
    if (O == null)
      throw Error("React.cloneElement(...): The argument must be a React element, but you passed " + O + ".");
    var Me = $({}, O.props), ft = O.key, vt = O.ref, Ge = O._owner;
    if (q != null) {
      if (q.ref !== void 0 && (vt = q.ref, Ge = at.current), q.key !== void 0 && (ft = "" + q.key), O.type && O.type.defaultProps)
        var St = O.type.defaultProps;
      for (ht in q)
        ke.call(q, ht) && !Ye.hasOwnProperty(ht) && (Me[ht] = q[ht] === void 0 && St !== void 0 ? St[ht] : q[ht]);
    }
    var ht = arguments.length - 2;
    if (ht === 1)
      Me.children = Re;
    else if (1 < ht) {
      St = Array(ht);
      for (var Wt = 0; Wt < ht; Wt++)
        St[Wt] = arguments[Wt + 2];
      Me.children = St;
    }
    return { $$typeof: S, type: O.type, key: ft, ref: vt, props: Me, _owner: Ge };
  }, Ut.createContext = function(O) {
    return O = { $$typeof: y, _currentValue: O, _currentValue2: O, _threadCount: 0, Provider: null, Consumer: null, _defaultValue: null, _globalName: null }, O.Provider = { $$typeof: W, _context: O }, O.Consumer = O;
  }, Ut.createElement = be, Ut.createFactory = function(O) {
    var q = be.bind(null, O);
    return q.type = O, q;
  }, Ut.createRef = function() {
    return { current: null };
  }, Ut.forwardRef = function(O) {
    return { $$typeof: ce, render: O };
  }, Ut.isValidElement = $e, Ut.lazy = function(O) {
    return { $$typeof: ye, _payload: { _status: -1, _result: O }, _init: yt };
  }, Ut.memo = function(O, q) {
    return { $$typeof: K, type: O, compare: q === void 0 ? null : q };
  }, Ut.startTransition = function(O) {
    var q = I.transition;
    I.transition = {};
    try {
      O();
    } finally {
      I.transition = q;
    }
  }, Ut.unstable_act = pe, Ut.useCallback = function(O, q) {
    return Se.current.useCallback(O, q);
  }, Ut.useContext = function(O) {
    return Se.current.useContext(O);
  }, Ut.useDebugValue = function() {
  }, Ut.useDeferredValue = function(O) {
    return Se.current.useDeferredValue(O);
  }, Ut.useEffect = function(O, q) {
    return Se.current.useEffect(O, q);
  }, Ut.useId = function() {
    return Se.current.useId();
  }, Ut.useImperativeHandle = function(O, q, Re) {
    return Se.current.useImperativeHandle(O, q, Re);
  }, Ut.useInsertionEffect = function(O, q) {
    return Se.current.useInsertionEffect(O, q);
  }, Ut.useLayoutEffect = function(O, q) {
    return Se.current.useLayoutEffect(O, q);
  }, Ut.useMemo = function(O, q) {
    return Se.current.useMemo(O, q);
  }, Ut.useReducer = function(O, q, Re) {
    return Se.current.useReducer(O, q, Re);
  }, Ut.useRef = function(O) {
    return Se.current.useRef(O);
  }, Ut.useState = function(O) {
    return Se.current.useState(O);
  }, Ut.useSyncExternalStore = function(O, q, Re) {
    return Se.current.useSyncExternalStore(O, q, Re);
  }, Ut.useTransition = function() {
    return Se.current.useTransition();
  }, Ut.version = "18.3.1", Ut;
}
var vv = { exports: {} };
/**
 * @license React
 * react.development.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
vv.exports;
var TE;
function Q_() {
  return TE || (TE = 1, function(S, w) {
    process.env.NODE_ENV !== "production" && function() {
      typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ < "u" && typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.registerInternalModuleStart == "function" && __REACT_DEVTOOLS_GLOBAL_HOOK__.registerInternalModuleStart(new Error());
      var b = "18.3.1", U = Symbol.for("react.element"), X = Symbol.for("react.portal"), W = Symbol.for("react.fragment"), y = Symbol.for("react.strict_mode"), ce = Symbol.for("react.profiler"), B = Symbol.for("react.provider"), K = Symbol.for("react.context"), ye = Symbol.for("react.forward_ref"), ne = Symbol.for("react.suspense"), oe = Symbol.for("react.suspense_list"), V = Symbol.for("react.memo"), $ = Symbol.for("react.lazy"), de = Symbol.for("react.offscreen"), Ae = Symbol.iterator, Dt = "@@iterator";
      function rt(h) {
        if (h === null || typeof h != "object")
          return null;
        var R = Ae && h[Ae] || h[Dt];
        return typeof R == "function" ? R : null;
      }
      var Ke = {
        /**
         * @internal
         * @type {ReactComponent}
         */
        current: null
      }, ct = {
        transition: null
      }, ke = {
        current: null,
        // Used to reproduce behavior of `batchedUpdates` in legacy mode.
        isBatchingLegacy: !1,
        didScheduleLegacyUpdate: !1
      }, at = {
        /**
         * @internal
         * @type {ReactComponent}
         */
        current: null
      }, Ye = {}, be = null;
      function Oe(h) {
        be = h;
      }
      Ye.setExtraStackFrame = function(h) {
        be = h;
      }, Ye.getCurrentStack = null, Ye.getStackAddendum = function() {
        var h = "";
        be && (h += be);
        var R = Ye.getCurrentStack;
        return R && (h += R() || ""), h;
      };
      var $e = !1, it = !1, Rt = !1, Ie = !1, st = !1, Nt = {
        ReactCurrentDispatcher: Ke,
        ReactCurrentBatchConfig: ct,
        ReactCurrentOwner: at
      };
      Nt.ReactDebugCurrentFrame = Ye, Nt.ReactCurrentActQueue = ke;
      function yt(h) {
        {
          for (var R = arguments.length, F = new Array(R > 1 ? R - 1 : 0), Y = 1; Y < R; Y++)
            F[Y - 1] = arguments[Y];
          I("warn", h, F);
        }
      }
      function Se(h) {
        {
          for (var R = arguments.length, F = new Array(R > 1 ? R - 1 : 0), Y = 1; Y < R; Y++)
            F[Y - 1] = arguments[Y];
          I("error", h, F);
        }
      }
      function I(h, R, F) {
        {
          var Y = Nt.ReactDebugCurrentFrame, ue = Y.getStackAddendum();
          ue !== "" && (R += "%s", F = F.concat([ue]));
          var et = F.map(function(me) {
            return String(me);
          });
          et.unshift("Warning: " + R), Function.prototype.apply.call(console[h], console, et);
        }
      }
      var Ue = {};
      function pe(h, R) {
        {
          var F = h.constructor, Y = F && (F.displayName || F.name) || "ReactClass", ue = Y + "." + R;
          if (Ue[ue])
            return;
          Se("Can't call %s on a component that is not yet mounted. This is a no-op, but it might indicate a bug in your application. Instead, assign to `this.state` directly or define a `state = {};` class property with the desired state in the %s component.", R, Y), Ue[ue] = !0;
        }
      }
      var O = {
        /**
         * Checks whether or not this composite component is mounted.
         * @param {ReactClass} publicInstance The instance we want to test.
         * @return {boolean} True if mounted, false otherwise.
         * @protected
         * @final
         */
        isMounted: function(h) {
          return !1;
        },
        /**
         * Forces an update. This should only be invoked when it is known with
         * certainty that we are **not** in a DOM transaction.
         *
         * You may want to call this when you know that some deeper aspect of the
         * component's state has changed but `setState` was not called.
         *
         * This will not invoke `shouldComponentUpdate`, but it will invoke
         * `componentWillUpdate` and `componentDidUpdate`.
         *
         * @param {ReactClass} publicInstance The instance that should rerender.
         * @param {?function} callback Called after component is updated.
         * @param {?string} callerName name of the calling function in the public API.
         * @internal
         */
        enqueueForceUpdate: function(h, R, F) {
          pe(h, "forceUpdate");
        },
        /**
         * Replaces all of the state. Always use this or `setState` to mutate state.
         * You should treat `this.state` as immutable.
         *
         * There is no guarantee that `this.state` will be immediately updated, so
         * accessing `this.state` after calling this method may return the old value.
         *
         * @param {ReactClass} publicInstance The instance that should rerender.
         * @param {object} completeState Next state.
         * @param {?function} callback Called after component is updated.
         * @param {?string} callerName name of the calling function in the public API.
         * @internal
         */
        enqueueReplaceState: function(h, R, F, Y) {
          pe(h, "replaceState");
        },
        /**
         * Sets a subset of the state. This only exists because _pendingState is
         * internal. This provides a merging strategy that is not available to deep
         * properties which is confusing. TODO: Expose pendingState or don't use it
         * during the merge.
         *
         * @param {ReactClass} publicInstance The instance that should rerender.
         * @param {object} partialState Next partial state to be merged with state.
         * @param {?function} callback Called after component is updated.
         * @param {?string} Name of the calling function in the public API.
         * @internal
         */
        enqueueSetState: function(h, R, F, Y) {
          pe(h, "setState");
        }
      }, q = Object.assign, Re = {};
      Object.freeze(Re);
      function Me(h, R, F) {
        this.props = h, this.context = R, this.refs = Re, this.updater = F || O;
      }
      Me.prototype.isReactComponent = {}, Me.prototype.setState = function(h, R) {
        if (typeof h != "object" && typeof h != "function" && h != null)
          throw new Error("setState(...): takes an object of state variables to update or a function which returns an object of state variables.");
        this.updater.enqueueSetState(this, h, R, "setState");
      }, Me.prototype.forceUpdate = function(h) {
        this.updater.enqueueForceUpdate(this, h, "forceUpdate");
      };
      {
        var ft = {
          isMounted: ["isMounted", "Instead, make sure to clean up subscriptions and pending requests in componentWillUnmount to prevent memory leaks."],
          replaceState: ["replaceState", "Refactor your code to use setState instead (see https://github.com/facebook/react/issues/3236)."]
        }, vt = function(h, R) {
          Object.defineProperty(Me.prototype, h, {
            get: function() {
              yt("%s(...) is deprecated in plain JavaScript React classes. %s", R[0], R[1]);
            }
          });
        };
        for (var Ge in ft)
          ft.hasOwnProperty(Ge) && vt(Ge, ft[Ge]);
      }
      function St() {
      }
      St.prototype = Me.prototype;
      function ht(h, R, F) {
        this.props = h, this.context = R, this.refs = Re, this.updater = F || O;
      }
      var Wt = ht.prototype = new St();
      Wt.constructor = ht, q(Wt, Me.prototype), Wt.isPureReactComponent = !0;
      function Fn() {
        var h = {
          current: null
        };
        return Object.seal(h), h;
      }
      var Yn = Array.isArray;
      function xn(h) {
        return Yn(h);
      }
      function Zn(h) {
        {
          var R = typeof Symbol == "function" && Symbol.toStringTag, F = R && h[Symbol.toStringTag] || h.constructor.name || "Object";
          return F;
        }
      }
      function Wn(h) {
        try {
          return Hn(h), !1;
        } catch {
          return !0;
        }
      }
      function Hn(h) {
        return "" + h;
      }
      function Mn(h) {
        if (Wn(h))
          return Se("The provided key is an unsupported type %s. This value must be coerced to a string before before using it here.", Zn(h)), Hn(h);
      }
      function Gr(h, R, F) {
        var Y = h.displayName;
        if (Y)
          return Y;
        var ue = R.displayName || R.name || "";
        return ue !== "" ? F + "(" + ue + ")" : F;
      }
      function qr(h) {
        return h.displayName || "Context";
      }
      function er(h) {
        if (h == null)
          return null;
        if (typeof h.tag == "number" && Se("Received an unexpected object in getComponentNameFromType(). This is likely a bug in React. Please file an issue."), typeof h == "function")
          return h.displayName || h.name || null;
        if (typeof h == "string")
          return h;
        switch (h) {
          case W:
            return "Fragment";
          case X:
            return "Portal";
          case ce:
            return "Profiler";
          case y:
            return "StrictMode";
          case ne:
            return "Suspense";
          case oe:
            return "SuspenseList";
        }
        if (typeof h == "object")
          switch (h.$$typeof) {
            case K:
              var R = h;
              return qr(R) + ".Consumer";
            case B:
              var F = h;
              return qr(F._context) + ".Provider";
            case ye:
              return Gr(h, h.render, "ForwardRef");
            case V:
              var Y = h.displayName || null;
              return Y !== null ? Y : er(h.type) || "Memo";
            case $: {
              var ue = h, et = ue._payload, me = ue._init;
              try {
                return er(me(et));
              } catch {
                return null;
              }
            }
          }
        return null;
      }
      var Cr = Object.prototype.hasOwnProperty, Xr = {
        key: !0,
        ref: !0,
        __self: !0,
        __source: !0
      }, Er, ya, sr;
      sr = {};
      function Kr(h) {
        if (Cr.call(h, "ref")) {
          var R = Object.getOwnPropertyDescriptor(h, "ref").get;
          if (R && R.isReactWarning)
            return !1;
        }
        return h.ref !== void 0;
      }
      function bn(h) {
        if (Cr.call(h, "key")) {
          var R = Object.getOwnPropertyDescriptor(h, "key").get;
          if (R && R.isReactWarning)
            return !1;
        }
        return h.key !== void 0;
      }
      function Or(h, R) {
        var F = function() {
          Er || (Er = !0, Se("%s: `key` is not a prop. Trying to access it will result in `undefined` being returned. If you need to access the same value within the child component, you should pass it as a different prop. (https://reactjs.org/link/special-props)", R));
        };
        F.isReactWarning = !0, Object.defineProperty(h, "key", {
          get: F,
          configurable: !0
        });
      }
      function mi(h, R) {
        var F = function() {
          ya || (ya = !0, Se("%s: `ref` is not a prop. Trying to access it will result in `undefined` being returned. If you need to access the same value within the child component, you should pass it as a different prop. (https://reactjs.org/link/special-props)", R));
        };
        F.isReactWarning = !0, Object.defineProperty(h, "ref", {
          get: F,
          configurable: !0
        });
      }
      function ga(h) {
        if (typeof h.ref == "string" && at.current && h.__self && at.current.stateNode !== h.__self) {
          var R = er(at.current.type);
          sr[R] || (Se('Component "%s" contains the string ref "%s". Support for string refs will be removed in a future major release. This case cannot be automatically converted to an arrow function. We ask you to manually fix this case by using useRef() or createRef() instead. Learn more about using refs safely here: https://reactjs.org/link/strict-mode-string-ref', R, h.ref), sr[R] = !0);
        }
      }
      var fe = function(h, R, F, Y, ue, et, me) {
        var Je = {
          // This tag allows us to uniquely identify this as a React Element
          $$typeof: U,
          // Built-in properties that belong on the element
          type: h,
          key: R,
          ref: F,
          props: me,
          // Record the component responsible for creating this element.
          _owner: et
        };
        return Je._store = {}, Object.defineProperty(Je._store, "validated", {
          configurable: !1,
          enumerable: !1,
          writable: !0,
          value: !1
        }), Object.defineProperty(Je, "_self", {
          configurable: !1,
          enumerable: !1,
          writable: !1,
          value: Y
        }), Object.defineProperty(Je, "_source", {
          configurable: !1,
          enumerable: !1,
          writable: !1,
          value: ue
        }), Object.freeze && (Object.freeze(Je.props), Object.freeze(Je)), Je;
      };
      function We(h, R, F) {
        var Y, ue = {}, et = null, me = null, Je = null, kt = null;
        if (R != null) {
          Kr(R) && (me = R.ref, ga(R)), bn(R) && (Mn(R.key), et = "" + R.key), Je = R.__self === void 0 ? null : R.__self, kt = R.__source === void 0 ? null : R.__source;
          for (Y in R)
            Cr.call(R, Y) && !Xr.hasOwnProperty(Y) && (ue[Y] = R[Y]);
        }
        var Pt = arguments.length - 2;
        if (Pt === 1)
          ue.children = F;
        else if (Pt > 1) {
          for (var on = Array(Pt), nn = 0; nn < Pt; nn++)
            on[nn] = arguments[nn + 2];
          Object.freeze && Object.freeze(on), ue.children = on;
        }
        if (h && h.defaultProps) {
          var un = h.defaultProps;
          for (Y in un)
            ue[Y] === void 0 && (ue[Y] = un[Y]);
        }
        if (et || me) {
          var cn = typeof h == "function" ? h.displayName || h.name || "Unknown" : h;
          et && Or(ue, cn), me && mi(ue, cn);
        }
        return fe(h, et, me, Je, kt, at.current, ue);
      }
      function bt(h, R) {
        var F = fe(h.type, R, h.ref, h._self, h._source, h._owner, h.props);
        return F;
      }
      function Qt(h, R, F) {
        if (h == null)
          throw new Error("React.cloneElement(...): The argument must be a React element, but you passed " + h + ".");
        var Y, ue = q({}, h.props), et = h.key, me = h.ref, Je = h._self, kt = h._source, Pt = h._owner;
        if (R != null) {
          Kr(R) && (me = R.ref, Pt = at.current), bn(R) && (Mn(R.key), et = "" + R.key);
          var on;
          h.type && h.type.defaultProps && (on = h.type.defaultProps);
          for (Y in R)
            Cr.call(R, Y) && !Xr.hasOwnProperty(Y) && (R[Y] === void 0 && on !== void 0 ? ue[Y] = on[Y] : ue[Y] = R[Y]);
        }
        var nn = arguments.length - 2;
        if (nn === 1)
          ue.children = F;
        else if (nn > 1) {
          for (var un = Array(nn), cn = 0; cn < nn; cn++)
            un[cn] = arguments[cn + 2];
          ue.children = un;
        }
        return fe(h.type, et, me, Je, kt, Pt, ue);
      }
      function qt(h) {
        return typeof h == "object" && h !== null && h.$$typeof === U;
      }
      var Ln = ".", Cn = ":";
      function wr(h) {
        var R = /[=:]/g, F = {
          "=": "=0",
          ":": "=2"
        }, Y = h.replace(R, function(ue) {
          return F[ue];
        });
        return "$" + Y;
      }
      var tn = !1, Mr = /\/+/g;
      function Xt(h) {
        return h.replace(Mr, "$&/");
      }
      function Kt(h, R) {
        return typeof h == "object" && h !== null && h.key != null ? (Mn(h.key), wr("" + h.key)) : R.toString(36);
      }
      function ai(h, R, F, Y, ue) {
        var et = typeof h;
        (et === "undefined" || et === "boolean") && (h = null);
        var me = !1;
        if (h === null)
          me = !0;
        else
          switch (et) {
            case "string":
            case "number":
              me = !0;
              break;
            case "object":
              switch (h.$$typeof) {
                case U:
                case X:
                  me = !0;
              }
          }
        if (me) {
          var Je = h, kt = ue(Je), Pt = Y === "" ? Ln + Kt(Je, 0) : Y;
          if (xn(kt)) {
            var on = "";
            Pt != null && (on = Xt(Pt) + "/"), ai(kt, R, on, "", function(od) {
              return od;
            });
          } else
            kt != null && (qt(kt) && (kt.key && (!Je || Je.key !== kt.key) && Mn(kt.key), kt = bt(
              kt,
              // Keep both the (mapped) and old keys if they differ, just as
              // traverseAllChildren used to do for objects as children
              F + // $FlowFixMe Flow incorrectly thinks React.Portal doesn't have a key
              (kt.key && (!Je || Je.key !== kt.key) ? (
                // $FlowFixMe Flow incorrectly thinks existing element's key can be a number
                // eslint-disable-next-line react-internal/safe-string-coercion
                Xt("" + kt.key) + "/"
              ) : "") + Pt
            )), R.push(kt));
          return 1;
        }
        var nn, un, cn = 0, At = Y === "" ? Ln : Y + Cn;
        if (xn(h))
          for (var Vi = 0; Vi < h.length; Vi++)
            nn = h[Vi], un = At + Kt(nn, Vi), cn += ai(nn, R, F, un, ue);
        else {
          var Ko = rt(h);
          if (typeof Ko == "function") {
            var rs = h;
            Ko === rs.entries && (tn || yt("Using Maps as children is not supported. Use an array of keyed ReactElements instead."), tn = !0);
            for (var ld = Ko.call(rs), ui, as = 0; !(ui = ld.next()).done; )
              nn = ui.value, un = At + Kt(nn, as++), cn += ai(nn, R, F, un, ue);
          } else if (et === "object") {
            var is = String(h);
            throw new Error("Objects are not valid as a React child (found: " + (is === "[object Object]" ? "object with keys {" + Object.keys(h).join(", ") + "}" : is) + "). If you meant to render a collection of children, use an array instead.");
          }
        }
        return cn;
      }
      function La(h, R, F) {
        if (h == null)
          return h;
        var Y = [], ue = 0;
        return ai(h, Y, "", "", function(et) {
          return R.call(F, et, ue++);
        }), Y;
      }
      function pl(h) {
        var R = 0;
        return La(h, function() {
          R++;
        }), R;
      }
      function Kl(h, R, F) {
        La(h, function() {
          R.apply(this, arguments);
        }, F);
      }
      function Po(h) {
        return La(h, function(R) {
          return R;
        }) || [];
      }
      function Ui(h) {
        if (!qt(h))
          throw new Error("React.Children.only expected to receive a single React element child.");
        return h;
      }
      function vl(h) {
        var R = {
          $$typeof: K,
          // As a workaround to support multiple concurrent renderers, we categorize
          // some renderers as primary and others as secondary. We only expect
          // there to be two concurrent renderers at most: React Native (primary) and
          // Fabric (secondary); React DOM (primary) and React ART (secondary).
          // Secondary renderers store their context values on separate fields.
          _currentValue: h,
          _currentValue2: h,
          // Used to track how many concurrent renderers this context currently
          // supports within in a single renderer. Such as parallel server rendering.
          _threadCount: 0,
          // These are circular
          Provider: null,
          Consumer: null,
          // Add these to use same hidden class in VM as ServerContext
          _defaultValue: null,
          _globalName: null
        };
        R.Provider = {
          $$typeof: B,
          _context: R
        };
        var F = !1, Y = !1, ue = !1;
        {
          var et = {
            $$typeof: K,
            _context: R
          };
          Object.defineProperties(et, {
            Provider: {
              get: function() {
                return Y || (Y = !0, Se("Rendering <Context.Consumer.Provider> is not supported and will be removed in a future major release. Did you mean to render <Context.Provider> instead?")), R.Provider;
              },
              set: function(me) {
                R.Provider = me;
              }
            },
            _currentValue: {
              get: function() {
                return R._currentValue;
              },
              set: function(me) {
                R._currentValue = me;
              }
            },
            _currentValue2: {
              get: function() {
                return R._currentValue2;
              },
              set: function(me) {
                R._currentValue2 = me;
              }
            },
            _threadCount: {
              get: function() {
                return R._threadCount;
              },
              set: function(me) {
                R._threadCount = me;
              }
            },
            Consumer: {
              get: function() {
                return F || (F = !0, Se("Rendering <Context.Consumer.Consumer> is not supported and will be removed in a future major release. Did you mean to render <Context.Consumer> instead?")), R.Consumer;
              }
            },
            displayName: {
              get: function() {
                return R.displayName;
              },
              set: function(me) {
                ue || (yt("Setting `displayName` on Context.Consumer has no effect. You should set it directly on the context with Context.displayName = '%s'.", me), ue = !0);
              }
            }
          }), R.Consumer = et;
        }
        return R._currentRenderer = null, R._currentRenderer2 = null, R;
      }
      var Sa = -1, yi = 0, xa = 1, ii = 2;
      function Lr(h) {
        if (h._status === Sa) {
          var R = h._result, F = R();
          if (F.then(function(et) {
            if (h._status === yi || h._status === Sa) {
              var me = h;
              me._status = xa, me._result = et;
            }
          }, function(et) {
            if (h._status === yi || h._status === Sa) {
              var me = h;
              me._status = ii, me._result = et;
            }
          }), h._status === Sa) {
            var Y = h;
            Y._status = yi, Y._result = F;
          }
        }
        if (h._status === xa) {
          var ue = h._result;
          return ue === void 0 && Se(`lazy: Expected the result of a dynamic import() call. Instead received: %s

Your code should look like: 
  const MyComponent = lazy(() => import('./MyComponent'))

Did you accidentally put curly braces around the import?`, ue), "default" in ue || Se(`lazy: Expected the result of a dynamic import() call. Instead received: %s

Your code should look like: 
  const MyComponent = lazy(() => import('./MyComponent'))`, ue), ue.default;
        } else
          throw h._result;
      }
      function ba(h) {
        var R = {
          // We use these fields to store the result.
          _status: Sa,
          _result: h
        }, F = {
          $$typeof: $,
          _payload: R,
          _init: Lr
        };
        {
          var Y, ue;
          Object.defineProperties(F, {
            defaultProps: {
              configurable: !0,
              get: function() {
                return Y;
              },
              set: function(et) {
                Se("React.lazy(...): It is not supported to assign `defaultProps` to a lazy component import. Either specify them where the component is defined, or create a wrapping component around it."), Y = et, Object.defineProperty(F, "defaultProps", {
                  enumerable: !0
                });
              }
            },
            propTypes: {
              configurable: !0,
              get: function() {
                return ue;
              },
              set: function(et) {
                Se("React.lazy(...): It is not supported to assign `propTypes` to a lazy component import. Either specify them where the component is defined, or create a wrapping component around it."), ue = et, Object.defineProperty(F, "propTypes", {
                  enumerable: !0
                });
              }
            }
          });
        }
        return F;
      }
      function gi(h) {
        h != null && h.$$typeof === V ? Se("forwardRef requires a render function but received a `memo` component. Instead of forwardRef(memo(...)), use memo(forwardRef(...)).") : typeof h != "function" ? Se("forwardRef requires a render function but was given %s.", h === null ? "null" : typeof h) : h.length !== 0 && h.length !== 2 && Se("forwardRef render functions accept exactly two parameters: props and ref. %s", h.length === 1 ? "Did you forget to use the ref parameter?" : "Any additional parameter will be undefined."), h != null && (h.defaultProps != null || h.propTypes != null) && Se("forwardRef render functions do not support propTypes or defaultProps. Did you accidentally pass a React component?");
        var R = {
          $$typeof: ye,
          render: h
        };
        {
          var F;
          Object.defineProperty(R, "displayName", {
            enumerable: !1,
            configurable: !0,
            get: function() {
              return F;
            },
            set: function(Y) {
              F = Y, !h.name && !h.displayName && (h.displayName = Y);
            }
          });
        }
        return R;
      }
      var Si;
      Si = Symbol.for("react.module.reference");
      function T(h) {
        return !!(typeof h == "string" || typeof h == "function" || h === W || h === ce || st || h === y || h === ne || h === oe || Ie || h === de || $e || it || Rt || typeof h == "object" && h !== null && (h.$$typeof === $ || h.$$typeof === V || h.$$typeof === B || h.$$typeof === K || h.$$typeof === ye || // This needs to include all possible module reference object
        // types supported by any Flight configuration anywhere since
        // we don't know which Flight build this will end up being used
        // with.
        h.$$typeof === Si || h.getModuleId !== void 0));
      }
      function ee(h, R) {
        T(h) || Se("memo: The first argument must be a component. Instead received: %s", h === null ? "null" : typeof h);
        var F = {
          $$typeof: V,
          type: h,
          compare: R === void 0 ? null : R
        };
        {
          var Y;
          Object.defineProperty(F, "displayName", {
            enumerable: !1,
            configurable: !0,
            get: function() {
              return Y;
            },
            set: function(ue) {
              Y = ue, !h.name && !h.displayName && (h.displayName = ue);
            }
          });
        }
        return F;
      }
      function ie() {
        var h = Ke.current;
        return h === null && Se(`Invalid hook call. Hooks can only be called inside of the body of a function component. This could happen for one of the following reasons:
1. You might have mismatching versions of React and the renderer (such as React DOM)
2. You might be breaking the Rules of Hooks
3. You might have more than one copy of React in the same app
See https://reactjs.org/link/invalid-hook-call for tips about how to debug and fix this problem.`), h;
      }
      function Pe(h) {
        var R = ie();
        if (h._context !== void 0) {
          var F = h._context;
          F.Consumer === h ? Se("Calling useContext(Context.Consumer) is not supported, may cause bugs, and will be removed in a future major release. Did you mean to call useContext(Context) instead?") : F.Provider === h && Se("Calling useContext(Context.Provider) is not supported. Did you mean to call useContext(Context) instead?");
        }
        return R.useContext(h);
      }
      function Tt(h) {
        var R = ie();
        return R.useState(h);
      }
      function jt(h, R, F) {
        var Y = ie();
        return Y.useReducer(h, R, F);
      }
      function Ze(h) {
        var R = ie();
        return R.useRef(h);
      }
      function Ct(h, R) {
        var F = ie();
        return F.useEffect(h, R);
      }
      function Pn(h, R) {
        var F = ie();
        return F.useInsertionEffect(h, R);
      }
      function ln(h, R) {
        var F = ie();
        return F.useLayoutEffect(h, R);
      }
      function dn(h, R) {
        var F = ie();
        return F.useCallback(h, R);
      }
      function Rr(h, R) {
        var F = ie();
        return F.useMemo(h, R);
      }
      function xi(h, R, F) {
        var Y = ie();
        return Y.useImperativeHandle(h, R, F);
      }
      function Vt(h, R) {
        {
          var F = ie();
          return F.useDebugValue(h, R);
        }
      }
      function tr() {
        var h = ie();
        return h.useTransition();
      }
      function jr(h) {
        var R = ie();
        return R.useDeferredValue(h);
      }
      function Et() {
        var h = ie();
        return h.useId();
      }
      function ja(h, R, F) {
        var Y = ie();
        return Y.useSyncExternalStore(h, R, F);
      }
      var hl = 0, Vo, ml, Jr, Zu, zr, es, ts;
      function cc() {
      }
      cc.__reactDisabledLog = !0;
      function Bo() {
        {
          if (hl === 0) {
            Vo = console.log, ml = console.info, Jr = console.warn, Zu = console.error, zr = console.group, es = console.groupCollapsed, ts = console.groupEnd;
            var h = {
              configurable: !0,
              enumerable: !0,
              value: cc,
              writable: !0
            };
            Object.defineProperties(console, {
              info: h,
              log: h,
              warn: h,
              error: h,
              group: h,
              groupCollapsed: h,
              groupEnd: h
            });
          }
          hl++;
        }
      }
      function yl() {
        {
          if (hl--, hl === 0) {
            var h = {
              configurable: !0,
              enumerable: !0,
              writable: !0
            };
            Object.defineProperties(console, {
              log: q({}, h, {
                value: Vo
              }),
              info: q({}, h, {
                value: ml
              }),
              warn: q({}, h, {
                value: Jr
              }),
              error: q({}, h, {
                value: Zu
              }),
              group: q({}, h, {
                value: zr
              }),
              groupCollapsed: q({}, h, {
                value: es
              }),
              groupEnd: q({}, h, {
                value: ts
              })
            });
          }
          hl < 0 && Se("disabledDepth fell below zero. This is a bug in React. Please file an issue.");
        }
      }
      var li = Nt.ReactCurrentDispatcher, Ar;
      function gl(h, R, F) {
        {
          if (Ar === void 0)
            try {
              throw Error();
            } catch (ue) {
              var Y = ue.stack.trim().match(/\n( *(at )?)/);
              Ar = Y && Y[1] || "";
            }
          return `
` + Ar + h;
        }
      }
      var Sl = !1, xl;
      {
        var $o = typeof WeakMap == "function" ? WeakMap : Map;
        xl = new $o();
      }
      function Io(h, R) {
        if (!h || Sl)
          return "";
        {
          var F = xl.get(h);
          if (F !== void 0)
            return F;
        }
        var Y;
        Sl = !0;
        var ue = Error.prepareStackTrace;
        Error.prepareStackTrace = void 0;
        var et;
        et = li.current, li.current = null, Bo();
        try {
          if (R) {
            var me = function() {
              throw Error();
            };
            if (Object.defineProperty(me.prototype, "props", {
              set: function() {
                throw Error();
              }
            }), typeof Reflect == "object" && Reflect.construct) {
              try {
                Reflect.construct(me, []);
              } catch (At) {
                Y = At;
              }
              Reflect.construct(h, [], me);
            } else {
              try {
                me.call();
              } catch (At) {
                Y = At;
              }
              h.call(me.prototype);
            }
          } else {
            try {
              throw Error();
            } catch (At) {
              Y = At;
            }
            h();
          }
        } catch (At) {
          if (At && Y && typeof At.stack == "string") {
            for (var Je = At.stack.split(`
`), kt = Y.stack.split(`
`), Pt = Je.length - 1, on = kt.length - 1; Pt >= 1 && on >= 0 && Je[Pt] !== kt[on]; )
              on--;
            for (; Pt >= 1 && on >= 0; Pt--, on--)
              if (Je[Pt] !== kt[on]) {
                if (Pt !== 1 || on !== 1)
                  do
                    if (Pt--, on--, on < 0 || Je[Pt] !== kt[on]) {
                      var nn = `
` + Je[Pt].replace(" at new ", " at ");
                      return h.displayName && nn.includes("<anonymous>") && (nn = nn.replace("<anonymous>", h.displayName)), typeof h == "function" && xl.set(h, nn), nn;
                    }
                  while (Pt >= 1 && on >= 0);
                break;
              }
          }
        } finally {
          Sl = !1, li.current = et, yl(), Error.prepareStackTrace = ue;
        }
        var un = h ? h.displayName || h.name : "", cn = un ? gl(un) : "";
        return typeof h == "function" && xl.set(h, cn), cn;
      }
      function Fi(h, R, F) {
        return Io(h, !1);
      }
      function id(h) {
        var R = h.prototype;
        return !!(R && R.isReactComponent);
      }
      function bi(h, R, F) {
        if (h == null)
          return "";
        if (typeof h == "function")
          return Io(h, id(h));
        if (typeof h == "string")
          return gl(h);
        switch (h) {
          case ne:
            return gl("Suspense");
          case oe:
            return gl("SuspenseList");
        }
        if (typeof h == "object")
          switch (h.$$typeof) {
            case ye:
              return Fi(h.render);
            case V:
              return bi(h.type, R, F);
            case $: {
              var Y = h, ue = Y._payload, et = Y._init;
              try {
                return bi(et(ue), R, F);
              } catch {
              }
            }
          }
        return "";
      }
      var Bt = {}, Yo = Nt.ReactDebugCurrentFrame;
      function Jl(h) {
        if (h) {
          var R = h._owner, F = bi(h.type, h._source, R ? R.type : null);
          Yo.setExtraStackFrame(F);
        } else
          Yo.setExtraStackFrame(null);
      }
      function Wo(h, R, F, Y, ue) {
        {
          var et = Function.call.bind(Cr);
          for (var me in h)
            if (et(h, me)) {
              var Je = void 0;
              try {
                if (typeof h[me] != "function") {
                  var kt = Error((Y || "React class") + ": " + F + " type `" + me + "` is invalid; it must be a function, usually from the `prop-types` package, but received `" + typeof h[me] + "`.This often happens because of typos such as `PropTypes.function` instead of `PropTypes.func`.");
                  throw kt.name = "Invariant Violation", kt;
                }
                Je = h[me](R, me, Y, F, null, "SECRET_DO_NOT_PASS_THIS_OR_YOU_WILL_BE_FIRED");
              } catch (Pt) {
                Je = Pt;
              }
              Je && !(Je instanceof Error) && (Jl(ue), Se("%s: type specification of %s `%s` is invalid; the type checker function must return `null` or an `Error` but returned a %s. You may have forgotten to pass an argument to the type checker creator (arrayOf, instanceOf, objectOf, oneOf, oneOfType, and shape all require an argument).", Y || "React class", F, me, typeof Je), Jl(null)), Je instanceof Error && !(Je.message in Bt) && (Bt[Je.message] = !0, Jl(ue), Se("Failed %s type: %s", F, Je.message), Jl(null));
            }
        }
      }
      function zt(h) {
        if (h) {
          var R = h._owner, F = bi(h.type, h._source, R ? R.type : null);
          Oe(F);
        } else
          Oe(null);
      }
      var Qo;
      Qo = !1;
      function Go() {
        if (at.current) {
          var h = er(at.current.type);
          if (h)
            return `

Check the render method of \`` + h + "`.";
        }
        return "";
      }
      function dt(h) {
        if (h !== void 0) {
          var R = h.fileName.replace(/^.*[\\\/]/, ""), F = h.lineNumber;
          return `

Check your code at ` + R + ":" + F + ".";
        }
        return "";
      }
      function Zl(h) {
        return h != null ? dt(h.__source) : "";
      }
      var En = {};
      function Zr(h) {
        var R = Go();
        if (!R) {
          var F = typeof h == "string" ? h : h.displayName || h.name;
          F && (R = `

Check the top-level render call using <` + F + ">.");
        }
        return R;
      }
      function Ur(h, R) {
        if (!(!h._store || h._store.validated || h.key != null)) {
          h._store.validated = !0;
          var F = Zr(R);
          if (!En[F]) {
            En[F] = !0;
            var Y = "";
            h && h._owner && h._owner !== at.current && (Y = " It was passed a child from " + er(h._owner.type) + "."), zt(h), Se('Each child in a list should have a unique "key" prop.%s%s See https://reactjs.org/link/warning-keys for more information.', F, Y), zt(null);
          }
        }
      }
      function bl(h, R) {
        if (typeof h == "object") {
          if (xn(h))
            for (var F = 0; F < h.length; F++) {
              var Y = h[F];
              qt(Y) && Ur(Y, R);
            }
          else if (qt(h))
            h._store && (h._store.validated = !0);
          else if (h) {
            var ue = rt(h);
            if (typeof ue == "function" && ue !== h.entries)
              for (var et = ue.call(h), me; !(me = et.next()).done; )
                qt(me.value) && Ur(me.value, R);
          }
        }
      }
      function kn(h) {
        {
          var R = h.type;
          if (R == null || typeof R == "string")
            return;
          var F;
          if (typeof R == "function")
            F = R.propTypes;
          else if (typeof R == "object" && (R.$$typeof === ye || // Note: Memo only checks outer props here.
          // Inner props are checked in the reconciler.
          R.$$typeof === V))
            F = R.propTypes;
          else
            return;
          if (F) {
            var Y = er(R);
            Wo(F, h.props, "prop", Y, h);
          } else if (R.PropTypes !== void 0 && !Qo) {
            Qo = !0;
            var ue = er(R);
            Se("Component %s declared `PropTypes` instead of `propTypes`. Did you misspell the property assignment?", ue || "Unknown");
          }
          typeof R.getDefaultProps == "function" && !R.getDefaultProps.isReactClassApproved && Se("getDefaultProps is only used on classic React.createClass definitions. Use a static property named `defaultProps` instead.");
        }
      }
      function Jt(h) {
        {
          for (var R = Object.keys(h.props), F = 0; F < R.length; F++) {
            var Y = R[F];
            if (Y !== "children" && Y !== "key") {
              zt(h), Se("Invalid prop `%s` supplied to `React.Fragment`. React.Fragment can only have `key` and `children` props.", Y), zt(null);
              break;
            }
          }
          h.ref !== null && (zt(h), Se("Invalid attribute `ref` supplied to `React.Fragment`."), zt(null));
        }
      }
      function fc(h, R, F) {
        var Y = T(h);
        if (!Y) {
          var ue = "";
          (h === void 0 || typeof h == "object" && h !== null && Object.keys(h).length === 0) && (ue += " You likely forgot to export your component from the file it's defined in, or you might have mixed up default and named imports.");
          var et = Zl(R);
          et ? ue += et : ue += Go();
          var me;
          h === null ? me = "null" : xn(h) ? me = "array" : h !== void 0 && h.$$typeof === U ? (me = "<" + (er(h.type) || "Unknown") + " />", ue = " Did you accidentally export a JSX literal instead of a component?") : me = typeof h, Se("React.createElement: type is invalid -- expected a string (for built-in components) or a class/function (for composite components) but got: %s.%s", me, ue);
        }
        var Je = We.apply(this, arguments);
        if (Je == null)
          return Je;
        if (Y)
          for (var kt = 2; kt < arguments.length; kt++)
            bl(arguments[kt], h);
        return h === W ? Jt(Je) : kn(Je), Je;
      }
      var ea = !1;
      function nr(h) {
        var R = fc.bind(null, h);
        return R.type = h, ea || (ea = !0, yt("React.createFactory() is deprecated and will be removed in a future major release. Consider using JSX or use React.createElement() directly instead.")), Object.defineProperty(R, "type", {
          enumerable: !1,
          get: function() {
            return yt("Factory.type is deprecated. Access the class directly before passing it to createFactory."), Object.defineProperty(this, "type", {
              value: h
            }), h;
          }
        }), R;
      }
      function Ci(h, R, F) {
        for (var Y = Qt.apply(this, arguments), ue = 2; ue < arguments.length; ue++)
          bl(arguments[ue], Y.type);
        return kn(Y), Y;
      }
      function dc(h, R) {
        var F = ct.transition;
        ct.transition = {};
        var Y = ct.transition;
        ct.transition._updatedFibers = /* @__PURE__ */ new Set();
        try {
          h();
        } finally {
          if (ct.transition = F, F === null && Y._updatedFibers) {
            var ue = Y._updatedFibers.size;
            ue > 10 && yt("Detected a large number of updates inside startTransition. If this is due to a subscription please re-write it to use React provided hooks. Otherwise concurrent mode guarantees are off the table."), Y._updatedFibers.clear();
          }
        }
      }
      var Hi = !1, Cl = null;
      function pc(h) {
        if (Cl === null)
          try {
            var R = ("require" + Math.random()).slice(0, 7), F = S && S[R];
            Cl = F.call(S, "timers").setImmediate;
          } catch {
            Cl = function(ue) {
              Hi === !1 && (Hi = !0, typeof MessageChannel > "u" && Se("This browser does not have a MessageChannel implementation, so enqueuing tasks via await act(async () => ...) will fail. Please file an issue at https://github.com/facebook/react/issues if you encounter this warning."));
              var et = new MessageChannel();
              et.port1.onmessage = ue, et.port2.postMessage(void 0);
            };
          }
        return Cl(h);
      }
      var za = 0, El = !1;
      function Pi(h) {
        {
          var R = za;
          za++, ke.current === null && (ke.current = []);
          var F = ke.isBatchingLegacy, Y;
          try {
            if (ke.isBatchingLegacy = !0, Y = h(), !F && ke.didScheduleLegacyUpdate) {
              var ue = ke.current;
              ue !== null && (ke.didScheduleLegacyUpdate = !1, Rl(ue));
            }
          } catch (un) {
            throw Aa(R), un;
          } finally {
            ke.isBatchingLegacy = F;
          }
          if (Y !== null && typeof Y == "object" && typeof Y.then == "function") {
            var et = Y, me = !1, Je = {
              then: function(un, cn) {
                me = !0, et.then(function(At) {
                  Aa(R), za === 0 ? qo(At, un, cn) : un(At);
                }, function(At) {
                  Aa(R), cn(At);
                });
              }
            };
            return !El && typeof Promise < "u" && Promise.resolve().then(function() {
            }).then(function() {
              me || (El = !0, Se("You called act(async () => ...) without await. This could lead to unexpected testing behaviour, interleaving multiple act calls and mixing their scopes. You should - await act(async () => ...);"));
            }), Je;
          } else {
            var kt = Y;
            if (Aa(R), za === 0) {
              var Pt = ke.current;
              Pt !== null && (Rl(Pt), ke.current = null);
              var on = {
                then: function(un, cn) {
                  ke.current === null ? (ke.current = [], qo(kt, un, cn)) : un(kt);
                }
              };
              return on;
            } else {
              var nn = {
                then: function(un, cn) {
                  un(kt);
                }
              };
              return nn;
            }
          }
        }
      }
      function Aa(h) {
        h !== za - 1 && Se("You seem to have overlapping act() calls, this is not supported. Be sure to await previous act() calls before making a new one. "), za = h;
      }
      function qo(h, R, F) {
        {
          var Y = ke.current;
          if (Y !== null)
            try {
              Rl(Y), pc(function() {
                Y.length === 0 ? (ke.current = null, R(h)) : qo(h, R, F);
              });
            } catch (ue) {
              F(ue);
            }
          else
            R(h);
        }
      }
      var wl = !1;
      function Rl(h) {
        if (!wl) {
          wl = !0;
          var R = 0;
          try {
            for (; R < h.length; R++) {
              var F = h[R];
              do
                F = F(!0);
              while (F !== null);
            }
            h.length = 0;
          } catch (Y) {
            throw h = h.slice(R + 1), Y;
          } finally {
            wl = !1;
          }
        }
      }
      var eo = fc, Xo = Ci, ns = nr, oi = {
        map: La,
        forEach: Kl,
        count: pl,
        toArray: Po,
        only: Ui
      };
      w.Children = oi, w.Component = Me, w.Fragment = W, w.Profiler = ce, w.PureComponent = ht, w.StrictMode = y, w.Suspense = ne, w.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED = Nt, w.act = Pi, w.cloneElement = Xo, w.createContext = vl, w.createElement = eo, w.createFactory = ns, w.createRef = Fn, w.forwardRef = gi, w.isValidElement = qt, w.lazy = ba, w.memo = ee, w.startTransition = dc, w.unstable_act = Pi, w.useCallback = dn, w.useContext = Pe, w.useDebugValue = Vt, w.useDeferredValue = jr, w.useEffect = Ct, w.useId = Et, w.useImperativeHandle = xi, w.useInsertionEffect = Pn, w.useLayoutEffect = ln, w.useMemo = Rr, w.useReducer = jt, w.useRef = Ze, w.useState = Tt, w.useSyncExternalStore = ja, w.useTransition = tr, w.version = b, typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ < "u" && typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.registerInternalModuleStop == "function" && __REACT_DEVTOOLS_GLOBAL_HOOK__.registerInternalModuleStop(new Error());
    }();
  }(vv, vv.exports)), vv.exports;
}
process.env.NODE_ENV === "production" ? HS.exports = W_() : HS.exports = Q_();
var wt = HS.exports;
const G_ = /* @__PURE__ */ Y_(wt);
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var kE;
function q_() {
  if (kE)
    return uv;
  kE = 1;
  var S = wt, w = Symbol.for("react.element"), b = Symbol.for("react.fragment"), U = Object.prototype.hasOwnProperty, X = S.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, W = { key: !0, ref: !0, __self: !0, __source: !0 };
  function y(ce, B, K) {
    var ye, ne = {}, oe = null, V = null;
    K !== void 0 && (oe = "" + K), B.key !== void 0 && (oe = "" + B.key), B.ref !== void 0 && (V = B.ref);
    for (ye in B)
      U.call(B, ye) && !W.hasOwnProperty(ye) && (ne[ye] = B[ye]);
    if (ce && ce.defaultProps)
      for (ye in B = ce.defaultProps, B)
        ne[ye] === void 0 && (ne[ye] = B[ye]);
    return { $$typeof: w, type: ce, key: oe, ref: V, props: ne, _owner: X.current };
  }
  return uv.Fragment = b, uv.jsx = y, uv.jsxs = y, uv;
}
var sv = {};
/**
 * @license React
 * react-jsx-runtime.development.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var _E;
function X_() {
  return _E || (_E = 1, process.env.NODE_ENV !== "production" && function() {
    var S = wt, w = Symbol.for("react.element"), b = Symbol.for("react.portal"), U = Symbol.for("react.fragment"), X = Symbol.for("react.strict_mode"), W = Symbol.for("react.profiler"), y = Symbol.for("react.provider"), ce = Symbol.for("react.context"), B = Symbol.for("react.forward_ref"), K = Symbol.for("react.suspense"), ye = Symbol.for("react.suspense_list"), ne = Symbol.for("react.memo"), oe = Symbol.for("react.lazy"), V = Symbol.for("react.offscreen"), $ = Symbol.iterator, de = "@@iterator";
    function Ae(T) {
      if (T === null || typeof T != "object")
        return null;
      var ee = $ && T[$] || T[de];
      return typeof ee == "function" ? ee : null;
    }
    var Dt = S.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED;
    function rt(T) {
      {
        for (var ee = arguments.length, ie = new Array(ee > 1 ? ee - 1 : 0), Pe = 1; Pe < ee; Pe++)
          ie[Pe - 1] = arguments[Pe];
        Ke("error", T, ie);
      }
    }
    function Ke(T, ee, ie) {
      {
        var Pe = Dt.ReactDebugCurrentFrame, Tt = Pe.getStackAddendum();
        Tt !== "" && (ee += "%s", ie = ie.concat([Tt]));
        var jt = ie.map(function(Ze) {
          return String(Ze);
        });
        jt.unshift("Warning: " + ee), Function.prototype.apply.call(console[T], console, jt);
      }
    }
    var ct = !1, ke = !1, at = !1, Ye = !1, be = !1, Oe;
    Oe = Symbol.for("react.module.reference");
    function $e(T) {
      return !!(typeof T == "string" || typeof T == "function" || T === U || T === W || be || T === X || T === K || T === ye || Ye || T === V || ct || ke || at || typeof T == "object" && T !== null && (T.$$typeof === oe || T.$$typeof === ne || T.$$typeof === y || T.$$typeof === ce || T.$$typeof === B || // This needs to include all possible module reference object
      // types supported by any Flight configuration anywhere since
      // we don't know which Flight build this will end up being used
      // with.
      T.$$typeof === Oe || T.getModuleId !== void 0));
    }
    function it(T, ee, ie) {
      var Pe = T.displayName;
      if (Pe)
        return Pe;
      var Tt = ee.displayName || ee.name || "";
      return Tt !== "" ? ie + "(" + Tt + ")" : ie;
    }
    function Rt(T) {
      return T.displayName || "Context";
    }
    function Ie(T) {
      if (T == null)
        return null;
      if (typeof T.tag == "number" && rt("Received an unexpected object in getComponentNameFromType(). This is likely a bug in React. Please file an issue."), typeof T == "function")
        return T.displayName || T.name || null;
      if (typeof T == "string")
        return T;
      switch (T) {
        case U:
          return "Fragment";
        case b:
          return "Portal";
        case W:
          return "Profiler";
        case X:
          return "StrictMode";
        case K:
          return "Suspense";
        case ye:
          return "SuspenseList";
      }
      if (typeof T == "object")
        switch (T.$$typeof) {
          case ce:
            var ee = T;
            return Rt(ee) + ".Consumer";
          case y:
            var ie = T;
            return Rt(ie._context) + ".Provider";
          case B:
            return it(T, T.render, "ForwardRef");
          case ne:
            var Pe = T.displayName || null;
            return Pe !== null ? Pe : Ie(T.type) || "Memo";
          case oe: {
            var Tt = T, jt = Tt._payload, Ze = Tt._init;
            try {
              return Ie(Ze(jt));
            } catch {
              return null;
            }
          }
        }
      return null;
    }
    var st = Object.assign, Nt = 0, yt, Se, I, Ue, pe, O, q;
    function Re() {
    }
    Re.__reactDisabledLog = !0;
    function Me() {
      {
        if (Nt === 0) {
          yt = console.log, Se = console.info, I = console.warn, Ue = console.error, pe = console.group, O = console.groupCollapsed, q = console.groupEnd;
          var T = {
            configurable: !0,
            enumerable: !0,
            value: Re,
            writable: !0
          };
          Object.defineProperties(console, {
            info: T,
            log: T,
            warn: T,
            error: T,
            group: T,
            groupCollapsed: T,
            groupEnd: T
          });
        }
        Nt++;
      }
    }
    function ft() {
      {
        if (Nt--, Nt === 0) {
          var T = {
            configurable: !0,
            enumerable: !0,
            writable: !0
          };
          Object.defineProperties(console, {
            log: st({}, T, {
              value: yt
            }),
            info: st({}, T, {
              value: Se
            }),
            warn: st({}, T, {
              value: I
            }),
            error: st({}, T, {
              value: Ue
            }),
            group: st({}, T, {
              value: pe
            }),
            groupCollapsed: st({}, T, {
              value: O
            }),
            groupEnd: st({}, T, {
              value: q
            })
          });
        }
        Nt < 0 && rt("disabledDepth fell below zero. This is a bug in React. Please file an issue.");
      }
    }
    var vt = Dt.ReactCurrentDispatcher, Ge;
    function St(T, ee, ie) {
      {
        if (Ge === void 0)
          try {
            throw Error();
          } catch (Tt) {
            var Pe = Tt.stack.trim().match(/\n( *(at )?)/);
            Ge = Pe && Pe[1] || "";
          }
        return `
` + Ge + T;
      }
    }
    var ht = !1, Wt;
    {
      var Fn = typeof WeakMap == "function" ? WeakMap : Map;
      Wt = new Fn();
    }
    function Yn(T, ee) {
      if (!T || ht)
        return "";
      {
        var ie = Wt.get(T);
        if (ie !== void 0)
          return ie;
      }
      var Pe;
      ht = !0;
      var Tt = Error.prepareStackTrace;
      Error.prepareStackTrace = void 0;
      var jt;
      jt = vt.current, vt.current = null, Me();
      try {
        if (ee) {
          var Ze = function() {
            throw Error();
          };
          if (Object.defineProperty(Ze.prototype, "props", {
            set: function() {
              throw Error();
            }
          }), typeof Reflect == "object" && Reflect.construct) {
            try {
              Reflect.construct(Ze, []);
            } catch (tr) {
              Pe = tr;
            }
            Reflect.construct(T, [], Ze);
          } else {
            try {
              Ze.call();
            } catch (tr) {
              Pe = tr;
            }
            T.call(Ze.prototype);
          }
        } else {
          try {
            throw Error();
          } catch (tr) {
            Pe = tr;
          }
          T();
        }
      } catch (tr) {
        if (tr && Pe && typeof tr.stack == "string") {
          for (var Ct = tr.stack.split(`
`), Pn = Pe.stack.split(`
`), ln = Ct.length - 1, dn = Pn.length - 1; ln >= 1 && dn >= 0 && Ct[ln] !== Pn[dn]; )
            dn--;
          for (; ln >= 1 && dn >= 0; ln--, dn--)
            if (Ct[ln] !== Pn[dn]) {
              if (ln !== 1 || dn !== 1)
                do
                  if (ln--, dn--, dn < 0 || Ct[ln] !== Pn[dn]) {
                    var Rr = `
` + Ct[ln].replace(" at new ", " at ");
                    return T.displayName && Rr.includes("<anonymous>") && (Rr = Rr.replace("<anonymous>", T.displayName)), typeof T == "function" && Wt.set(T, Rr), Rr;
                  }
                while (ln >= 1 && dn >= 0);
              break;
            }
        }
      } finally {
        ht = !1, vt.current = jt, ft(), Error.prepareStackTrace = Tt;
      }
      var xi = T ? T.displayName || T.name : "", Vt = xi ? St(xi) : "";
      return typeof T == "function" && Wt.set(T, Vt), Vt;
    }
    function xn(T, ee, ie) {
      return Yn(T, !1);
    }
    function Zn(T) {
      var ee = T.prototype;
      return !!(ee && ee.isReactComponent);
    }
    function Wn(T, ee, ie) {
      if (T == null)
        return "";
      if (typeof T == "function")
        return Yn(T, Zn(T));
      if (typeof T == "string")
        return St(T);
      switch (T) {
        case K:
          return St("Suspense");
        case ye:
          return St("SuspenseList");
      }
      if (typeof T == "object")
        switch (T.$$typeof) {
          case B:
            return xn(T.render);
          case ne:
            return Wn(T.type, ee, ie);
          case oe: {
            var Pe = T, Tt = Pe._payload, jt = Pe._init;
            try {
              return Wn(jt(Tt), ee, ie);
            } catch {
            }
          }
        }
      return "";
    }
    var Hn = Object.prototype.hasOwnProperty, Mn = {}, Gr = Dt.ReactDebugCurrentFrame;
    function qr(T) {
      if (T) {
        var ee = T._owner, ie = Wn(T.type, T._source, ee ? ee.type : null);
        Gr.setExtraStackFrame(ie);
      } else
        Gr.setExtraStackFrame(null);
    }
    function er(T, ee, ie, Pe, Tt) {
      {
        var jt = Function.call.bind(Hn);
        for (var Ze in T)
          if (jt(T, Ze)) {
            var Ct = void 0;
            try {
              if (typeof T[Ze] != "function") {
                var Pn = Error((Pe || "React class") + ": " + ie + " type `" + Ze + "` is invalid; it must be a function, usually from the `prop-types` package, but received `" + typeof T[Ze] + "`.This often happens because of typos such as `PropTypes.function` instead of `PropTypes.func`.");
                throw Pn.name = "Invariant Violation", Pn;
              }
              Ct = T[Ze](ee, Ze, Pe, ie, null, "SECRET_DO_NOT_PASS_THIS_OR_YOU_WILL_BE_FIRED");
            } catch (ln) {
              Ct = ln;
            }
            Ct && !(Ct instanceof Error) && (qr(Tt), rt("%s: type specification of %s `%s` is invalid; the type checker function must return `null` or an `Error` but returned a %s. You may have forgotten to pass an argument to the type checker creator (arrayOf, instanceOf, objectOf, oneOf, oneOfType, and shape all require an argument).", Pe || "React class", ie, Ze, typeof Ct), qr(null)), Ct instanceof Error && !(Ct.message in Mn) && (Mn[Ct.message] = !0, qr(Tt), rt("Failed %s type: %s", ie, Ct.message), qr(null));
          }
      }
    }
    var Cr = Array.isArray;
    function Xr(T) {
      return Cr(T);
    }
    function Er(T) {
      {
        var ee = typeof Symbol == "function" && Symbol.toStringTag, ie = ee && T[Symbol.toStringTag] || T.constructor.name || "Object";
        return ie;
      }
    }
    function ya(T) {
      try {
        return sr(T), !1;
      } catch {
        return !0;
      }
    }
    function sr(T) {
      return "" + T;
    }
    function Kr(T) {
      if (ya(T))
        return rt("The provided key is an unsupported type %s. This value must be coerced to a string before before using it here.", Er(T)), sr(T);
    }
    var bn = Dt.ReactCurrentOwner, Or = {
      key: !0,
      ref: !0,
      __self: !0,
      __source: !0
    }, mi, ga, fe;
    fe = {};
    function We(T) {
      if (Hn.call(T, "ref")) {
        var ee = Object.getOwnPropertyDescriptor(T, "ref").get;
        if (ee && ee.isReactWarning)
          return !1;
      }
      return T.ref !== void 0;
    }
    function bt(T) {
      if (Hn.call(T, "key")) {
        var ee = Object.getOwnPropertyDescriptor(T, "key").get;
        if (ee && ee.isReactWarning)
          return !1;
      }
      return T.key !== void 0;
    }
    function Qt(T, ee) {
      if (typeof T.ref == "string" && bn.current && ee && bn.current.stateNode !== ee) {
        var ie = Ie(bn.current.type);
        fe[ie] || (rt('Component "%s" contains the string ref "%s". Support for string refs will be removed in a future major release. This case cannot be automatically converted to an arrow function. We ask you to manually fix this case by using useRef() or createRef() instead. Learn more about using refs safely here: https://reactjs.org/link/strict-mode-string-ref', Ie(bn.current.type), T.ref), fe[ie] = !0);
      }
    }
    function qt(T, ee) {
      {
        var ie = function() {
          mi || (mi = !0, rt("%s: `key` is not a prop. Trying to access it will result in `undefined` being returned. If you need to access the same value within the child component, you should pass it as a different prop. (https://reactjs.org/link/special-props)", ee));
        };
        ie.isReactWarning = !0, Object.defineProperty(T, "key", {
          get: ie,
          configurable: !0
        });
      }
    }
    function Ln(T, ee) {
      {
        var ie = function() {
          ga || (ga = !0, rt("%s: `ref` is not a prop. Trying to access it will result in `undefined` being returned. If you need to access the same value within the child component, you should pass it as a different prop. (https://reactjs.org/link/special-props)", ee));
        };
        ie.isReactWarning = !0, Object.defineProperty(T, "ref", {
          get: ie,
          configurable: !0
        });
      }
    }
    var Cn = function(T, ee, ie, Pe, Tt, jt, Ze) {
      var Ct = {
        // This tag allows us to uniquely identify this as a React Element
        $$typeof: w,
        // Built-in properties that belong on the element
        type: T,
        key: ee,
        ref: ie,
        props: Ze,
        // Record the component responsible for creating this element.
        _owner: jt
      };
      return Ct._store = {}, Object.defineProperty(Ct._store, "validated", {
        configurable: !1,
        enumerable: !1,
        writable: !0,
        value: !1
      }), Object.defineProperty(Ct, "_self", {
        configurable: !1,
        enumerable: !1,
        writable: !1,
        value: Pe
      }), Object.defineProperty(Ct, "_source", {
        configurable: !1,
        enumerable: !1,
        writable: !1,
        value: Tt
      }), Object.freeze && (Object.freeze(Ct.props), Object.freeze(Ct)), Ct;
    };
    function wr(T, ee, ie, Pe, Tt) {
      {
        var jt, Ze = {}, Ct = null, Pn = null;
        ie !== void 0 && (Kr(ie), Ct = "" + ie), bt(ee) && (Kr(ee.key), Ct = "" + ee.key), We(ee) && (Pn = ee.ref, Qt(ee, Tt));
        for (jt in ee)
          Hn.call(ee, jt) && !Or.hasOwnProperty(jt) && (Ze[jt] = ee[jt]);
        if (T && T.defaultProps) {
          var ln = T.defaultProps;
          for (jt in ln)
            Ze[jt] === void 0 && (Ze[jt] = ln[jt]);
        }
        if (Ct || Pn) {
          var dn = typeof T == "function" ? T.displayName || T.name || "Unknown" : T;
          Ct && qt(Ze, dn), Pn && Ln(Ze, dn);
        }
        return Cn(T, Ct, Pn, Tt, Pe, bn.current, Ze);
      }
    }
    var tn = Dt.ReactCurrentOwner, Mr = Dt.ReactDebugCurrentFrame;
    function Xt(T) {
      if (T) {
        var ee = T._owner, ie = Wn(T.type, T._source, ee ? ee.type : null);
        Mr.setExtraStackFrame(ie);
      } else
        Mr.setExtraStackFrame(null);
    }
    var Kt;
    Kt = !1;
    function ai(T) {
      return typeof T == "object" && T !== null && T.$$typeof === w;
    }
    function La() {
      {
        if (tn.current) {
          var T = Ie(tn.current.type);
          if (T)
            return `

Check the render method of \`` + T + "`.";
        }
        return "";
      }
    }
    function pl(T) {
      {
        if (T !== void 0) {
          var ee = T.fileName.replace(/^.*[\\\/]/, ""), ie = T.lineNumber;
          return `

Check your code at ` + ee + ":" + ie + ".";
        }
        return "";
      }
    }
    var Kl = {};
    function Po(T) {
      {
        var ee = La();
        if (!ee) {
          var ie = typeof T == "string" ? T : T.displayName || T.name;
          ie && (ee = `

Check the top-level render call using <` + ie + ">.");
        }
        return ee;
      }
    }
    function Ui(T, ee) {
      {
        if (!T._store || T._store.validated || T.key != null)
          return;
        T._store.validated = !0;
        var ie = Po(ee);
        if (Kl[ie])
          return;
        Kl[ie] = !0;
        var Pe = "";
        T && T._owner && T._owner !== tn.current && (Pe = " It was passed a child from " + Ie(T._owner.type) + "."), Xt(T), rt('Each child in a list should have a unique "key" prop.%s%s See https://reactjs.org/link/warning-keys for more information.', ie, Pe), Xt(null);
      }
    }
    function vl(T, ee) {
      {
        if (typeof T != "object")
          return;
        if (Xr(T))
          for (var ie = 0; ie < T.length; ie++) {
            var Pe = T[ie];
            ai(Pe) && Ui(Pe, ee);
          }
        else if (ai(T))
          T._store && (T._store.validated = !0);
        else if (T) {
          var Tt = Ae(T);
          if (typeof Tt == "function" && Tt !== T.entries)
            for (var jt = Tt.call(T), Ze; !(Ze = jt.next()).done; )
              ai(Ze.value) && Ui(Ze.value, ee);
        }
      }
    }
    function Sa(T) {
      {
        var ee = T.type;
        if (ee == null || typeof ee == "string")
          return;
        var ie;
        if (typeof ee == "function")
          ie = ee.propTypes;
        else if (typeof ee == "object" && (ee.$$typeof === B || // Note: Memo only checks outer props here.
        // Inner props are checked in the reconciler.
        ee.$$typeof === ne))
          ie = ee.propTypes;
        else
          return;
        if (ie) {
          var Pe = Ie(ee);
          er(ie, T.props, "prop", Pe, T);
        } else if (ee.PropTypes !== void 0 && !Kt) {
          Kt = !0;
          var Tt = Ie(ee);
          rt("Component %s declared `PropTypes` instead of `propTypes`. Did you misspell the property assignment?", Tt || "Unknown");
        }
        typeof ee.getDefaultProps == "function" && !ee.getDefaultProps.isReactClassApproved && rt("getDefaultProps is only used on classic React.createClass definitions. Use a static property named `defaultProps` instead.");
      }
    }
    function yi(T) {
      {
        for (var ee = Object.keys(T.props), ie = 0; ie < ee.length; ie++) {
          var Pe = ee[ie];
          if (Pe !== "children" && Pe !== "key") {
            Xt(T), rt("Invalid prop `%s` supplied to `React.Fragment`. React.Fragment can only have `key` and `children` props.", Pe), Xt(null);
            break;
          }
        }
        T.ref !== null && (Xt(T), rt("Invalid attribute `ref` supplied to `React.Fragment`."), Xt(null));
      }
    }
    var xa = {};
    function ii(T, ee, ie, Pe, Tt, jt) {
      {
        var Ze = $e(T);
        if (!Ze) {
          var Ct = "";
          (T === void 0 || typeof T == "object" && T !== null && Object.keys(T).length === 0) && (Ct += " You likely forgot to export your component from the file it's defined in, or you might have mixed up default and named imports.");
          var Pn = pl(Tt);
          Pn ? Ct += Pn : Ct += La();
          var ln;
          T === null ? ln = "null" : Xr(T) ? ln = "array" : T !== void 0 && T.$$typeof === w ? (ln = "<" + (Ie(T.type) || "Unknown") + " />", Ct = " Did you accidentally export a JSX literal instead of a component?") : ln = typeof T, rt("React.jsx: type is invalid -- expected a string (for built-in components) or a class/function (for composite components) but got: %s.%s", ln, Ct);
        }
        var dn = wr(T, ee, ie, Tt, jt);
        if (dn == null)
          return dn;
        if (Ze) {
          var Rr = ee.children;
          if (Rr !== void 0)
            if (Pe)
              if (Xr(Rr)) {
                for (var xi = 0; xi < Rr.length; xi++)
                  vl(Rr[xi], T);
                Object.freeze && Object.freeze(Rr);
              } else
                rt("React.jsx: Static children should always be an array. You are likely explicitly calling React.jsxs or React.jsxDEV. Use the Babel transform instead.");
            else
              vl(Rr, T);
        }
        if (Hn.call(ee, "key")) {
          var Vt = Ie(T), tr = Object.keys(ee).filter(function(ja) {
            return ja !== "key";
          }), jr = tr.length > 0 ? "{key: someKey, " + tr.join(": ..., ") + ": ...}" : "{key: someKey}";
          if (!xa[Vt + jr]) {
            var Et = tr.length > 0 ? "{" + tr.join(": ..., ") + ": ...}" : "{}";
            rt(`A props object containing a "key" prop is being spread into JSX:
  let props = %s;
  <%s {...props} />
React keys must be passed directly to JSX without using spread:
  let props = %s;
  <%s key={someKey} {...props} />`, jr, Vt, Et, Vt), xa[Vt + jr] = !0;
          }
        }
        return T === U ? yi(dn) : Sa(dn), dn;
      }
    }
    function Lr(T, ee, ie) {
      return ii(T, ee, ie, !0);
    }
    function ba(T, ee, ie) {
      return ii(T, ee, ie, !1);
    }
    var gi = ba, Si = Lr;
    sv.Fragment = U, sv.jsx = gi, sv.jsxs = Si;
  }()), sv;
}
process.env.NODE_ENV === "production" ? FS.exports = q_() : FS.exports = X_();
var C = FS.exports, hv = {}, PS = { exports: {} }, ni = {}, iy = { exports: {} }, jS = {};
/**
 * @license React
 * scheduler.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var DE;
function K_() {
  return DE || (DE = 1, function(S) {
    function w(I, Ue) {
      var pe = I.length;
      I.push(Ue);
      e:
        for (; 0 < pe; ) {
          var O = pe - 1 >>> 1, q = I[O];
          if (0 < X(q, Ue))
            I[O] = Ue, I[pe] = q, pe = O;
          else
            break e;
        }
    }
    function b(I) {
      return I.length === 0 ? null : I[0];
    }
    function U(I) {
      if (I.length === 0)
        return null;
      var Ue = I[0], pe = I.pop();
      if (pe !== Ue) {
        I[0] = pe;
        e:
          for (var O = 0, q = I.length, Re = q >>> 1; O < Re; ) {
            var Me = 2 * (O + 1) - 1, ft = I[Me], vt = Me + 1, Ge = I[vt];
            if (0 > X(ft, pe))
              vt < q && 0 > X(Ge, ft) ? (I[O] = Ge, I[vt] = pe, O = vt) : (I[O] = ft, I[Me] = pe, O = Me);
            else if (vt < q && 0 > X(Ge, pe))
              I[O] = Ge, I[vt] = pe, O = vt;
            else
              break e;
          }
      }
      return Ue;
    }
    function X(I, Ue) {
      var pe = I.sortIndex - Ue.sortIndex;
      return pe !== 0 ? pe : I.id - Ue.id;
    }
    if (typeof performance == "object" && typeof performance.now == "function") {
      var W = performance;
      S.unstable_now = function() {
        return W.now();
      };
    } else {
      var y = Date, ce = y.now();
      S.unstable_now = function() {
        return y.now() - ce;
      };
    }
    var B = [], K = [], ye = 1, ne = null, oe = 3, V = !1, $ = !1, de = !1, Ae = typeof setTimeout == "function" ? setTimeout : null, Dt = typeof clearTimeout == "function" ? clearTimeout : null, rt = typeof setImmediate < "u" ? setImmediate : null;
    typeof navigator < "u" && navigator.scheduling !== void 0 && navigator.scheduling.isInputPending !== void 0 && navigator.scheduling.isInputPending.bind(navigator.scheduling);
    function Ke(I) {
      for (var Ue = b(K); Ue !== null; ) {
        if (Ue.callback === null)
          U(K);
        else if (Ue.startTime <= I)
          U(K), Ue.sortIndex = Ue.expirationTime, w(B, Ue);
        else
          break;
        Ue = b(K);
      }
    }
    function ct(I) {
      if (de = !1, Ke(I), !$)
        if (b(B) !== null)
          $ = !0, yt(ke);
        else {
          var Ue = b(K);
          Ue !== null && Se(ct, Ue.startTime - I);
        }
    }
    function ke(I, Ue) {
      $ = !1, de && (de = !1, Dt(be), be = -1), V = !0;
      var pe = oe;
      try {
        for (Ke(Ue), ne = b(B); ne !== null && (!(ne.expirationTime > Ue) || I && !it()); ) {
          var O = ne.callback;
          if (typeof O == "function") {
            ne.callback = null, oe = ne.priorityLevel;
            var q = O(ne.expirationTime <= Ue);
            Ue = S.unstable_now(), typeof q == "function" ? ne.callback = q : ne === b(B) && U(B), Ke(Ue);
          } else
            U(B);
          ne = b(B);
        }
        if (ne !== null)
          var Re = !0;
        else {
          var Me = b(K);
          Me !== null && Se(ct, Me.startTime - Ue), Re = !1;
        }
        return Re;
      } finally {
        ne = null, oe = pe, V = !1;
      }
    }
    var at = !1, Ye = null, be = -1, Oe = 5, $e = -1;
    function it() {
      return !(S.unstable_now() - $e < Oe);
    }
    function Rt() {
      if (Ye !== null) {
        var I = S.unstable_now();
        $e = I;
        var Ue = !0;
        try {
          Ue = Ye(!0, I);
        } finally {
          Ue ? Ie() : (at = !1, Ye = null);
        }
      } else
        at = !1;
    }
    var Ie;
    if (typeof rt == "function")
      Ie = function() {
        rt(Rt);
      };
    else if (typeof MessageChannel < "u") {
      var st = new MessageChannel(), Nt = st.port2;
      st.port1.onmessage = Rt, Ie = function() {
        Nt.postMessage(null);
      };
    } else
      Ie = function() {
        Ae(Rt, 0);
      };
    function yt(I) {
      Ye = I, at || (at = !0, Ie());
    }
    function Se(I, Ue) {
      be = Ae(function() {
        I(S.unstable_now());
      }, Ue);
    }
    S.unstable_IdlePriority = 5, S.unstable_ImmediatePriority = 1, S.unstable_LowPriority = 4, S.unstable_NormalPriority = 3, S.unstable_Profiling = null, S.unstable_UserBlockingPriority = 2, S.unstable_cancelCallback = function(I) {
      I.callback = null;
    }, S.unstable_continueExecution = function() {
      $ || V || ($ = !0, yt(ke));
    }, S.unstable_forceFrameRate = function(I) {
      0 > I || 125 < I ? console.error("forceFrameRate takes a positive int between 0 and 125, forcing frame rates higher than 125 fps is not supported") : Oe = 0 < I ? Math.floor(1e3 / I) : 5;
    }, S.unstable_getCurrentPriorityLevel = function() {
      return oe;
    }, S.unstable_getFirstCallbackNode = function() {
      return b(B);
    }, S.unstable_next = function(I) {
      switch (oe) {
        case 1:
        case 2:
        case 3:
          var Ue = 3;
          break;
        default:
          Ue = oe;
      }
      var pe = oe;
      oe = Ue;
      try {
        return I();
      } finally {
        oe = pe;
      }
    }, S.unstable_pauseExecution = function() {
    }, S.unstable_requestPaint = function() {
    }, S.unstable_runWithPriority = function(I, Ue) {
      switch (I) {
        case 1:
        case 2:
        case 3:
        case 4:
        case 5:
          break;
        default:
          I = 3;
      }
      var pe = oe;
      oe = I;
      try {
        return Ue();
      } finally {
        oe = pe;
      }
    }, S.unstable_scheduleCallback = function(I, Ue, pe) {
      var O = S.unstable_now();
      switch (typeof pe == "object" && pe !== null ? (pe = pe.delay, pe = typeof pe == "number" && 0 < pe ? O + pe : O) : pe = O, I) {
        case 1:
          var q = -1;
          break;
        case 2:
          q = 250;
          break;
        case 5:
          q = 1073741823;
          break;
        case 4:
          q = 1e4;
          break;
        default:
          q = 5e3;
      }
      return q = pe + q, I = { id: ye++, callback: Ue, priorityLevel: I, startTime: pe, expirationTime: q, sortIndex: -1 }, pe > O ? (I.sortIndex = pe, w(K, I), b(B) === null && I === b(K) && (de ? (Dt(be), be = -1) : de = !0, Se(ct, pe - O))) : (I.sortIndex = q, w(B, I), $ || V || ($ = !0, yt(ke))), I;
    }, S.unstable_shouldYield = it, S.unstable_wrapCallback = function(I) {
      var Ue = oe;
      return function() {
        var pe = oe;
        oe = Ue;
        try {
          return I.apply(this, arguments);
        } finally {
          oe = pe;
        }
      };
    };
  }(jS)), jS;
}
var zS = {};
/**
 * @license React
 * scheduler.development.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var NE;
function J_() {
  return NE || (NE = 1, function(S) {
    process.env.NODE_ENV !== "production" && function() {
      typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ < "u" && typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.registerInternalModuleStart == "function" && __REACT_DEVTOOLS_GLOBAL_HOOK__.registerInternalModuleStart(new Error());
      var w = !1, b = !1, U = 5;
      function X(fe, We) {
        var bt = fe.length;
        fe.push(We), ce(fe, We, bt);
      }
      function W(fe) {
        return fe.length === 0 ? null : fe[0];
      }
      function y(fe) {
        if (fe.length === 0)
          return null;
        var We = fe[0], bt = fe.pop();
        return bt !== We && (fe[0] = bt, B(fe, bt, 0)), We;
      }
      function ce(fe, We, bt) {
        for (var Qt = bt; Qt > 0; ) {
          var qt = Qt - 1 >>> 1, Ln = fe[qt];
          if (K(Ln, We) > 0)
            fe[qt] = We, fe[Qt] = Ln, Qt = qt;
          else
            return;
        }
      }
      function B(fe, We, bt) {
        for (var Qt = bt, qt = fe.length, Ln = qt >>> 1; Qt < Ln; ) {
          var Cn = (Qt + 1) * 2 - 1, wr = fe[Cn], tn = Cn + 1, Mr = fe[tn];
          if (K(wr, We) < 0)
            tn < qt && K(Mr, wr) < 0 ? (fe[Qt] = Mr, fe[tn] = We, Qt = tn) : (fe[Qt] = wr, fe[Cn] = We, Qt = Cn);
          else if (tn < qt && K(Mr, We) < 0)
            fe[Qt] = Mr, fe[tn] = We, Qt = tn;
          else
            return;
        }
      }
      function K(fe, We) {
        var bt = fe.sortIndex - We.sortIndex;
        return bt !== 0 ? bt : fe.id - We.id;
      }
      var ye = 1, ne = 2, oe = 3, V = 4, $ = 5;
      function de(fe, We) {
      }
      var Ae = typeof performance == "object" && typeof performance.now == "function";
      if (Ae) {
        var Dt = performance;
        S.unstable_now = function() {
          return Dt.now();
        };
      } else {
        var rt = Date, Ke = rt.now();
        S.unstable_now = function() {
          return rt.now() - Ke;
        };
      }
      var ct = 1073741823, ke = -1, at = 250, Ye = 5e3, be = 1e4, Oe = ct, $e = [], it = [], Rt = 1, Ie = null, st = oe, Nt = !1, yt = !1, Se = !1, I = typeof setTimeout == "function" ? setTimeout : null, Ue = typeof clearTimeout == "function" ? clearTimeout : null, pe = typeof setImmediate < "u" ? setImmediate : null;
      typeof navigator < "u" && navigator.scheduling !== void 0 && navigator.scheduling.isInputPending !== void 0 && navigator.scheduling.isInputPending.bind(navigator.scheduling);
      function O(fe) {
        for (var We = W(it); We !== null; ) {
          if (We.callback === null)
            y(it);
          else if (We.startTime <= fe)
            y(it), We.sortIndex = We.expirationTime, X($e, We);
          else
            return;
          We = W(it);
        }
      }
      function q(fe) {
        if (Se = !1, O(fe), !yt)
          if (W($e) !== null)
            yt = !0, Kr(Re);
          else {
            var We = W(it);
            We !== null && bn(q, We.startTime - fe);
          }
      }
      function Re(fe, We) {
        yt = !1, Se && (Se = !1, Or()), Nt = !0;
        var bt = st;
        try {
          var Qt;
          if (!b)
            return Me(fe, We);
        } finally {
          Ie = null, st = bt, Nt = !1;
        }
      }
      function Me(fe, We) {
        var bt = We;
        for (O(bt), Ie = W($e); Ie !== null && !w && !(Ie.expirationTime > bt && (!fe || qr())); ) {
          var Qt = Ie.callback;
          if (typeof Qt == "function") {
            Ie.callback = null, st = Ie.priorityLevel;
            var qt = Ie.expirationTime <= bt, Ln = Qt(qt);
            bt = S.unstable_now(), typeof Ln == "function" ? Ie.callback = Ln : Ie === W($e) && y($e), O(bt);
          } else
            y($e);
          Ie = W($e);
        }
        if (Ie !== null)
          return !0;
        var Cn = W(it);
        return Cn !== null && bn(q, Cn.startTime - bt), !1;
      }
      function ft(fe, We) {
        switch (fe) {
          case ye:
          case ne:
          case oe:
          case V:
          case $:
            break;
          default:
            fe = oe;
        }
        var bt = st;
        st = fe;
        try {
          return We();
        } finally {
          st = bt;
        }
      }
      function vt(fe) {
        var We;
        switch (st) {
          case ye:
          case ne:
          case oe:
            We = oe;
            break;
          default:
            We = st;
            break;
        }
        var bt = st;
        st = We;
        try {
          return fe();
        } finally {
          st = bt;
        }
      }
      function Ge(fe) {
        var We = st;
        return function() {
          var bt = st;
          st = We;
          try {
            return fe.apply(this, arguments);
          } finally {
            st = bt;
          }
        };
      }
      function St(fe, We, bt) {
        var Qt = S.unstable_now(), qt;
        if (typeof bt == "object" && bt !== null) {
          var Ln = bt.delay;
          typeof Ln == "number" && Ln > 0 ? qt = Qt + Ln : qt = Qt;
        } else
          qt = Qt;
        var Cn;
        switch (fe) {
          case ye:
            Cn = ke;
            break;
          case ne:
            Cn = at;
            break;
          case $:
            Cn = Oe;
            break;
          case V:
            Cn = be;
            break;
          case oe:
          default:
            Cn = Ye;
            break;
        }
        var wr = qt + Cn, tn = {
          id: Rt++,
          callback: We,
          priorityLevel: fe,
          startTime: qt,
          expirationTime: wr,
          sortIndex: -1
        };
        return qt > Qt ? (tn.sortIndex = qt, X(it, tn), W($e) === null && tn === W(it) && (Se ? Or() : Se = !0, bn(q, qt - Qt))) : (tn.sortIndex = wr, X($e, tn), !yt && !Nt && (yt = !0, Kr(Re))), tn;
      }
      function ht() {
      }
      function Wt() {
        !yt && !Nt && (yt = !0, Kr(Re));
      }
      function Fn() {
        return W($e);
      }
      function Yn(fe) {
        fe.callback = null;
      }
      function xn() {
        return st;
      }
      var Zn = !1, Wn = null, Hn = -1, Mn = U, Gr = -1;
      function qr() {
        var fe = S.unstable_now() - Gr;
        return !(fe < Mn);
      }
      function er() {
      }
      function Cr(fe) {
        if (fe < 0 || fe > 125) {
          console.error("forceFrameRate takes a positive int between 0 and 125, forcing frame rates higher than 125 fps is not supported");
          return;
        }
        fe > 0 ? Mn = Math.floor(1e3 / fe) : Mn = U;
      }
      var Xr = function() {
        if (Wn !== null) {
          var fe = S.unstable_now();
          Gr = fe;
          var We = !0, bt = !0;
          try {
            bt = Wn(We, fe);
          } finally {
            bt ? Er() : (Zn = !1, Wn = null);
          }
        } else
          Zn = !1;
      }, Er;
      if (typeof pe == "function")
        Er = function() {
          pe(Xr);
        };
      else if (typeof MessageChannel < "u") {
        var ya = new MessageChannel(), sr = ya.port2;
        ya.port1.onmessage = Xr, Er = function() {
          sr.postMessage(null);
        };
      } else
        Er = function() {
          I(Xr, 0);
        };
      function Kr(fe) {
        Wn = fe, Zn || (Zn = !0, Er());
      }
      function bn(fe, We) {
        Hn = I(function() {
          fe(S.unstable_now());
        }, We);
      }
      function Or() {
        Ue(Hn), Hn = -1;
      }
      var mi = er, ga = null;
      S.unstable_IdlePriority = $, S.unstable_ImmediatePriority = ye, S.unstable_LowPriority = V, S.unstable_NormalPriority = oe, S.unstable_Profiling = ga, S.unstable_UserBlockingPriority = ne, S.unstable_cancelCallback = Yn, S.unstable_continueExecution = Wt, S.unstable_forceFrameRate = Cr, S.unstable_getCurrentPriorityLevel = xn, S.unstable_getFirstCallbackNode = Fn, S.unstable_next = vt, S.unstable_pauseExecution = ht, S.unstable_requestPaint = mi, S.unstable_runWithPriority = ft, S.unstable_scheduleCallback = St, S.unstable_shouldYield = qr, S.unstable_wrapCallback = Ge, typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ < "u" && typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.registerInternalModuleStop == "function" && __REACT_DEVTOOLS_GLOBAL_HOOK__.registerInternalModuleStop(new Error());
    }();
  }(zS)), zS;
}
var OE;
function PE() {
  return OE || (OE = 1, process.env.NODE_ENV === "production" ? iy.exports = K_() : iy.exports = J_()), iy.exports;
}
/**
 * @license React
 * react-dom.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var ME;
function Z_() {
  if (ME)
    return ni;
  ME = 1;
  var S = wt, w = PE();
  function b(n) {
    for (var r = "https://reactjs.org/docs/error-decoder.html?invariant=" + n, l = 1; l < arguments.length; l++)
      r += "&args[]=" + encodeURIComponent(arguments[l]);
    return "Minified React error #" + n + "; visit " + r + " for the full message or use the non-minified dev environment for full errors and additional helpful warnings.";
  }
  var U = /* @__PURE__ */ new Set(), X = {};
  function W(n, r) {
    y(n, r), y(n + "Capture", r);
  }
  function y(n, r) {
    for (X[n] = r, n = 0; n < r.length; n++)
      U.add(r[n]);
  }
  var ce = !(typeof window > "u" || typeof window.document > "u" || typeof window.document.createElement > "u"), B = Object.prototype.hasOwnProperty, K = /^[:A-Z_a-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD][:A-Z_a-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD\-.0-9\u00B7\u0300-\u036F\u203F-\u2040]*$/, ye = {}, ne = {};
  function oe(n) {
    return B.call(ne, n) ? !0 : B.call(ye, n) ? !1 : K.test(n) ? ne[n] = !0 : (ye[n] = !0, !1);
  }
  function V(n, r, l, u) {
    if (l !== null && l.type === 0)
      return !1;
    switch (typeof r) {
      case "function":
      case "symbol":
        return !0;
      case "boolean":
        return u ? !1 : l !== null ? !l.acceptsBooleans : (n = n.toLowerCase().slice(0, 5), n !== "data-" && n !== "aria-");
      default:
        return !1;
    }
  }
  function $(n, r, l, u) {
    if (r === null || typeof r > "u" || V(n, r, l, u))
      return !0;
    if (u)
      return !1;
    if (l !== null)
      switch (l.type) {
        case 3:
          return !r;
        case 4:
          return r === !1;
        case 5:
          return isNaN(r);
        case 6:
          return isNaN(r) || 1 > r;
      }
    return !1;
  }
  function de(n, r, l, u, c, d, m) {
    this.acceptsBooleans = r === 2 || r === 3 || r === 4, this.attributeName = u, this.attributeNamespace = c, this.mustUseProperty = l, this.propertyName = n, this.type = r, this.sanitizeURL = d, this.removeEmptyString = m;
  }
  var Ae = {};
  "children dangerouslySetInnerHTML defaultValue defaultChecked innerHTML suppressContentEditableWarning suppressHydrationWarning style".split(" ").forEach(function(n) {
    Ae[n] = new de(n, 0, !1, n, null, !1, !1);
  }), [["acceptCharset", "accept-charset"], ["className", "class"], ["htmlFor", "for"], ["httpEquiv", "http-equiv"]].forEach(function(n) {
    var r = n[0];
    Ae[r] = new de(r, 1, !1, n[1], null, !1, !1);
  }), ["contentEditable", "draggable", "spellCheck", "value"].forEach(function(n) {
    Ae[n] = new de(n, 2, !1, n.toLowerCase(), null, !1, !1);
  }), ["autoReverse", "externalResourcesRequired", "focusable", "preserveAlpha"].forEach(function(n) {
    Ae[n] = new de(n, 2, !1, n, null, !1, !1);
  }), "allowFullScreen async autoFocus autoPlay controls default defer disabled disablePictureInPicture disableRemotePlayback formNoValidate hidden loop noModule noValidate open playsInline readOnly required reversed scoped seamless itemScope".split(" ").forEach(function(n) {
    Ae[n] = new de(n, 3, !1, n.toLowerCase(), null, !1, !1);
  }), ["checked", "multiple", "muted", "selected"].forEach(function(n) {
    Ae[n] = new de(n, 3, !0, n, null, !1, !1);
  }), ["capture", "download"].forEach(function(n) {
    Ae[n] = new de(n, 4, !1, n, null, !1, !1);
  }), ["cols", "rows", "size", "span"].forEach(function(n) {
    Ae[n] = new de(n, 6, !1, n, null, !1, !1);
  }), ["rowSpan", "start"].forEach(function(n) {
    Ae[n] = new de(n, 5, !1, n.toLowerCase(), null, !1, !1);
  });
  var Dt = /[\-:]([a-z])/g;
  function rt(n) {
    return n[1].toUpperCase();
  }
  "accent-height alignment-baseline arabic-form baseline-shift cap-height clip-path clip-rule color-interpolation color-interpolation-filters color-profile color-rendering dominant-baseline enable-background fill-opacity fill-rule flood-color flood-opacity font-family font-size font-size-adjust font-stretch font-style font-variant font-weight glyph-name glyph-orientation-horizontal glyph-orientation-vertical horiz-adv-x horiz-origin-x image-rendering letter-spacing lighting-color marker-end marker-mid marker-start overline-position overline-thickness paint-order panose-1 pointer-events rendering-intent shape-rendering stop-color stop-opacity strikethrough-position strikethrough-thickness stroke-dasharray stroke-dashoffset stroke-linecap stroke-linejoin stroke-miterlimit stroke-opacity stroke-width text-anchor text-decoration text-rendering underline-position underline-thickness unicode-bidi unicode-range units-per-em v-alphabetic v-hanging v-ideographic v-mathematical vector-effect vert-adv-y vert-origin-x vert-origin-y word-spacing writing-mode xmlns:xlink x-height".split(" ").forEach(function(n) {
    var r = n.replace(
      Dt,
      rt
    );
    Ae[r] = new de(r, 1, !1, n, null, !1, !1);
  }), "xlink:actuate xlink:arcrole xlink:role xlink:show xlink:title xlink:type".split(" ").forEach(function(n) {
    var r = n.replace(Dt, rt);
    Ae[r] = new de(r, 1, !1, n, "http://www.w3.org/1999/xlink", !1, !1);
  }), ["xml:base", "xml:lang", "xml:space"].forEach(function(n) {
    var r = n.replace(Dt, rt);
    Ae[r] = new de(r, 1, !1, n, "http://www.w3.org/XML/1998/namespace", !1, !1);
  }), ["tabIndex", "crossOrigin"].forEach(function(n) {
    Ae[n] = new de(n, 1, !1, n.toLowerCase(), null, !1, !1);
  }), Ae.xlinkHref = new de("xlinkHref", 1, !1, "xlink:href", "http://www.w3.org/1999/xlink", !0, !1), ["src", "href", "action", "formAction"].forEach(function(n) {
    Ae[n] = new de(n, 1, !1, n.toLowerCase(), null, !0, !0);
  });
  function Ke(n, r, l, u) {
    var c = Ae.hasOwnProperty(r) ? Ae[r] : null;
    (c !== null ? c.type !== 0 : u || !(2 < r.length) || r[0] !== "o" && r[0] !== "O" || r[1] !== "n" && r[1] !== "N") && ($(r, l, c, u) && (l = null), u || c === null ? oe(r) && (l === null ? n.removeAttribute(r) : n.setAttribute(r, "" + l)) : c.mustUseProperty ? n[c.propertyName] = l === null ? c.type === 3 ? !1 : "" : l : (r = c.attributeName, u = c.attributeNamespace, l === null ? n.removeAttribute(r) : (c = c.type, l = c === 3 || c === 4 && l === !0 ? "" : "" + l, u ? n.setAttributeNS(u, r, l) : n.setAttribute(r, l))));
  }
  var ct = S.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED, ke = Symbol.for("react.element"), at = Symbol.for("react.portal"), Ye = Symbol.for("react.fragment"), be = Symbol.for("react.strict_mode"), Oe = Symbol.for("react.profiler"), $e = Symbol.for("react.provider"), it = Symbol.for("react.context"), Rt = Symbol.for("react.forward_ref"), Ie = Symbol.for("react.suspense"), st = Symbol.for("react.suspense_list"), Nt = Symbol.for("react.memo"), yt = Symbol.for("react.lazy"), Se = Symbol.for("react.offscreen"), I = Symbol.iterator;
  function Ue(n) {
    return n === null || typeof n != "object" ? null : (n = I && n[I] || n["@@iterator"], typeof n == "function" ? n : null);
  }
  var pe = Object.assign, O;
  function q(n) {
    if (O === void 0)
      try {
        throw Error();
      } catch (l) {
        var r = l.stack.trim().match(/\n( *(at )?)/);
        O = r && r[1] || "";
      }
    return `
` + O + n;
  }
  var Re = !1;
  function Me(n, r) {
    if (!n || Re)
      return "";
    Re = !0;
    var l = Error.prepareStackTrace;
    Error.prepareStackTrace = void 0;
    try {
      if (r)
        if (r = function() {
          throw Error();
        }, Object.defineProperty(r.prototype, "props", { set: function() {
          throw Error();
        } }), typeof Reflect == "object" && Reflect.construct) {
          try {
            Reflect.construct(r, []);
          } catch (H) {
            var u = H;
          }
          Reflect.construct(n, [], r);
        } else {
          try {
            r.call();
          } catch (H) {
            u = H;
          }
          n.call(r.prototype);
        }
      else {
        try {
          throw Error();
        } catch (H) {
          u = H;
        }
        n();
      }
    } catch (H) {
      if (H && u && typeof H.stack == "string") {
        for (var c = H.stack.split(`
`), d = u.stack.split(`
`), m = c.length - 1, E = d.length - 1; 1 <= m && 0 <= E && c[m] !== d[E]; )
          E--;
        for (; 1 <= m && 0 <= E; m--, E--)
          if (c[m] !== d[E]) {
            if (m !== 1 || E !== 1)
              do
                if (m--, E--, 0 > E || c[m] !== d[E]) {
                  var k = `
` + c[m].replace(" at new ", " at ");
                  return n.displayName && k.includes("<anonymous>") && (k = k.replace("<anonymous>", n.displayName)), k;
                }
              while (1 <= m && 0 <= E);
            break;
          }
      }
    } finally {
      Re = !1, Error.prepareStackTrace = l;
    }
    return (n = n ? n.displayName || n.name : "") ? q(n) : "";
  }
  function ft(n) {
    switch (n.tag) {
      case 5:
        return q(n.type);
      case 16:
        return q("Lazy");
      case 13:
        return q("Suspense");
      case 19:
        return q("SuspenseList");
      case 0:
      case 2:
      case 15:
        return n = Me(n.type, !1), n;
      case 11:
        return n = Me(n.type.render, !1), n;
      case 1:
        return n = Me(n.type, !0), n;
      default:
        return "";
    }
  }
  function vt(n) {
    if (n == null)
      return null;
    if (typeof n == "function")
      return n.displayName || n.name || null;
    if (typeof n == "string")
      return n;
    switch (n) {
      case Ye:
        return "Fragment";
      case at:
        return "Portal";
      case Oe:
        return "Profiler";
      case be:
        return "StrictMode";
      case Ie:
        return "Suspense";
      case st:
        return "SuspenseList";
    }
    if (typeof n == "object")
      switch (n.$$typeof) {
        case it:
          return (n.displayName || "Context") + ".Consumer";
        case $e:
          return (n._context.displayName || "Context") + ".Provider";
        case Rt:
          var r = n.render;
          return n = n.displayName, n || (n = r.displayName || r.name || "", n = n !== "" ? "ForwardRef(" + n + ")" : "ForwardRef"), n;
        case Nt:
          return r = n.displayName || null, r !== null ? r : vt(n.type) || "Memo";
        case yt:
          r = n._payload, n = n._init;
          try {
            return vt(n(r));
          } catch {
          }
      }
    return null;
  }
  function Ge(n) {
    var r = n.type;
    switch (n.tag) {
      case 24:
        return "Cache";
      case 9:
        return (r.displayName || "Context") + ".Consumer";
      case 10:
        return (r._context.displayName || "Context") + ".Provider";
      case 18:
        return "DehydratedFragment";
      case 11:
        return n = r.render, n = n.displayName || n.name || "", r.displayName || (n !== "" ? "ForwardRef(" + n + ")" : "ForwardRef");
      case 7:
        return "Fragment";
      case 5:
        return r;
      case 4:
        return "Portal";
      case 3:
        return "Root";
      case 6:
        return "Text";
      case 16:
        return vt(r);
      case 8:
        return r === be ? "StrictMode" : "Mode";
      case 22:
        return "Offscreen";
      case 12:
        return "Profiler";
      case 21:
        return "Scope";
      case 13:
        return "Suspense";
      case 19:
        return "SuspenseList";
      case 25:
        return "TracingMarker";
      case 1:
      case 0:
      case 17:
      case 2:
      case 14:
      case 15:
        if (typeof r == "function")
          return r.displayName || r.name || null;
        if (typeof r == "string")
          return r;
    }
    return null;
  }
  function St(n) {
    switch (typeof n) {
      case "boolean":
      case "number":
      case "string":
      case "undefined":
        return n;
      case "object":
        return n;
      default:
        return "";
    }
  }
  function ht(n) {
    var r = n.type;
    return (n = n.nodeName) && n.toLowerCase() === "input" && (r === "checkbox" || r === "radio");
  }
  function Wt(n) {
    var r = ht(n) ? "checked" : "value", l = Object.getOwnPropertyDescriptor(n.constructor.prototype, r), u = "" + n[r];
    if (!n.hasOwnProperty(r) && typeof l < "u" && typeof l.get == "function" && typeof l.set == "function") {
      var c = l.get, d = l.set;
      return Object.defineProperty(n, r, { configurable: !0, get: function() {
        return c.call(this);
      }, set: function(m) {
        u = "" + m, d.call(this, m);
      } }), Object.defineProperty(n, r, { enumerable: l.enumerable }), { getValue: function() {
        return u;
      }, setValue: function(m) {
        u = "" + m;
      }, stopTracking: function() {
        n._valueTracker = null, delete n[r];
      } };
    }
  }
  function Fn(n) {
    n._valueTracker || (n._valueTracker = Wt(n));
  }
  function Yn(n) {
    if (!n)
      return !1;
    var r = n._valueTracker;
    if (!r)
      return !0;
    var l = r.getValue(), u = "";
    return n && (u = ht(n) ? n.checked ? "true" : "false" : n.value), n = u, n !== l ? (r.setValue(n), !0) : !1;
  }
  function xn(n) {
    if (n = n || (typeof document < "u" ? document : void 0), typeof n > "u")
      return null;
    try {
      return n.activeElement || n.body;
    } catch {
      return n.body;
    }
  }
  function Zn(n, r) {
    var l = r.checked;
    return pe({}, r, { defaultChecked: void 0, defaultValue: void 0, value: void 0, checked: l ?? n._wrapperState.initialChecked });
  }
  function Wn(n, r) {
    var l = r.defaultValue == null ? "" : r.defaultValue, u = r.checked != null ? r.checked : r.defaultChecked;
    l = St(r.value != null ? r.value : l), n._wrapperState = { initialChecked: u, initialValue: l, controlled: r.type === "checkbox" || r.type === "radio" ? r.checked != null : r.value != null };
  }
  function Hn(n, r) {
    r = r.checked, r != null && Ke(n, "checked", r, !1);
  }
  function Mn(n, r) {
    Hn(n, r);
    var l = St(r.value), u = r.type;
    if (l != null)
      u === "number" ? (l === 0 && n.value === "" || n.value != l) && (n.value = "" + l) : n.value !== "" + l && (n.value = "" + l);
    else if (u === "submit" || u === "reset") {
      n.removeAttribute("value");
      return;
    }
    r.hasOwnProperty("value") ? qr(n, r.type, l) : r.hasOwnProperty("defaultValue") && qr(n, r.type, St(r.defaultValue)), r.checked == null && r.defaultChecked != null && (n.defaultChecked = !!r.defaultChecked);
  }
  function Gr(n, r, l) {
    if (r.hasOwnProperty("value") || r.hasOwnProperty("defaultValue")) {
      var u = r.type;
      if (!(u !== "submit" && u !== "reset" || r.value !== void 0 && r.value !== null))
        return;
      r = "" + n._wrapperState.initialValue, l || r === n.value || (n.value = r), n.defaultValue = r;
    }
    l = n.name, l !== "" && (n.name = ""), n.defaultChecked = !!n._wrapperState.initialChecked, l !== "" && (n.name = l);
  }
  function qr(n, r, l) {
    (r !== "number" || xn(n.ownerDocument) !== n) && (l == null ? n.defaultValue = "" + n._wrapperState.initialValue : n.defaultValue !== "" + l && (n.defaultValue = "" + l));
  }
  var er = Array.isArray;
  function Cr(n, r, l, u) {
    if (n = n.options, r) {
      r = {};
      for (var c = 0; c < l.length; c++)
        r["$" + l[c]] = !0;
      for (l = 0; l < n.length; l++)
        c = r.hasOwnProperty("$" + n[l].value), n[l].selected !== c && (n[l].selected = c), c && u && (n[l].defaultSelected = !0);
    } else {
      for (l = "" + St(l), r = null, c = 0; c < n.length; c++) {
        if (n[c].value === l) {
          n[c].selected = !0, u && (n[c].defaultSelected = !0);
          return;
        }
        r !== null || n[c].disabled || (r = n[c]);
      }
      r !== null && (r.selected = !0);
    }
  }
  function Xr(n, r) {
    if (r.dangerouslySetInnerHTML != null)
      throw Error(b(91));
    return pe({}, r, { value: void 0, defaultValue: void 0, children: "" + n._wrapperState.initialValue });
  }
  function Er(n, r) {
    var l = r.value;
    if (l == null) {
      if (l = r.children, r = r.defaultValue, l != null) {
        if (r != null)
          throw Error(b(92));
        if (er(l)) {
          if (1 < l.length)
            throw Error(b(93));
          l = l[0];
        }
        r = l;
      }
      r == null && (r = ""), l = r;
    }
    n._wrapperState = { initialValue: St(l) };
  }
  function ya(n, r) {
    var l = St(r.value), u = St(r.defaultValue);
    l != null && (l = "" + l, l !== n.value && (n.value = l), r.defaultValue == null && n.defaultValue !== l && (n.defaultValue = l)), u != null && (n.defaultValue = "" + u);
  }
  function sr(n) {
    var r = n.textContent;
    r === n._wrapperState.initialValue && r !== "" && r !== null && (n.value = r);
  }
  function Kr(n) {
    switch (n) {
      case "svg":
        return "http://www.w3.org/2000/svg";
      case "math":
        return "http://www.w3.org/1998/Math/MathML";
      default:
        return "http://www.w3.org/1999/xhtml";
    }
  }
  function bn(n, r) {
    return n == null || n === "http://www.w3.org/1999/xhtml" ? Kr(r) : n === "http://www.w3.org/2000/svg" && r === "foreignObject" ? "http://www.w3.org/1999/xhtml" : n;
  }
  var Or, mi = function(n) {
    return typeof MSApp < "u" && MSApp.execUnsafeLocalFunction ? function(r, l, u, c) {
      MSApp.execUnsafeLocalFunction(function() {
        return n(r, l, u, c);
      });
    } : n;
  }(function(n, r) {
    if (n.namespaceURI !== "http://www.w3.org/2000/svg" || "innerHTML" in n)
      n.innerHTML = r;
    else {
      for (Or = Or || document.createElement("div"), Or.innerHTML = "<svg>" + r.valueOf().toString() + "</svg>", r = Or.firstChild; n.firstChild; )
        n.removeChild(n.firstChild);
      for (; r.firstChild; )
        n.appendChild(r.firstChild);
    }
  });
  function ga(n, r) {
    if (r) {
      var l = n.firstChild;
      if (l && l === n.lastChild && l.nodeType === 3) {
        l.nodeValue = r;
        return;
      }
    }
    n.textContent = r;
  }
  var fe = {
    animationIterationCount: !0,
    aspectRatio: !0,
    borderImageOutset: !0,
    borderImageSlice: !0,
    borderImageWidth: !0,
    boxFlex: !0,
    boxFlexGroup: !0,
    boxOrdinalGroup: !0,
    columnCount: !0,
    columns: !0,
    flex: !0,
    flexGrow: !0,
    flexPositive: !0,
    flexShrink: !0,
    flexNegative: !0,
    flexOrder: !0,
    gridArea: !0,
    gridRow: !0,
    gridRowEnd: !0,
    gridRowSpan: !0,
    gridRowStart: !0,
    gridColumn: !0,
    gridColumnEnd: !0,
    gridColumnSpan: !0,
    gridColumnStart: !0,
    fontWeight: !0,
    lineClamp: !0,
    lineHeight: !0,
    opacity: !0,
    order: !0,
    orphans: !0,
    tabSize: !0,
    widows: !0,
    zIndex: !0,
    zoom: !0,
    fillOpacity: !0,
    floodOpacity: !0,
    stopOpacity: !0,
    strokeDasharray: !0,
    strokeDashoffset: !0,
    strokeMiterlimit: !0,
    strokeOpacity: !0,
    strokeWidth: !0
  }, We = ["Webkit", "ms", "Moz", "O"];
  Object.keys(fe).forEach(function(n) {
    We.forEach(function(r) {
      r = r + n.charAt(0).toUpperCase() + n.substring(1), fe[r] = fe[n];
    });
  });
  function bt(n, r, l) {
    return r == null || typeof r == "boolean" || r === "" ? "" : l || typeof r != "number" || r === 0 || fe.hasOwnProperty(n) && fe[n] ? ("" + r).trim() : r + "px";
  }
  function Qt(n, r) {
    n = n.style;
    for (var l in r)
      if (r.hasOwnProperty(l)) {
        var u = l.indexOf("--") === 0, c = bt(l, r[l], u);
        l === "float" && (l = "cssFloat"), u ? n.setProperty(l, c) : n[l] = c;
      }
  }
  var qt = pe({ menuitem: !0 }, { area: !0, base: !0, br: !0, col: !0, embed: !0, hr: !0, img: !0, input: !0, keygen: !0, link: !0, meta: !0, param: !0, source: !0, track: !0, wbr: !0 });
  function Ln(n, r) {
    if (r) {
      if (qt[n] && (r.children != null || r.dangerouslySetInnerHTML != null))
        throw Error(b(137, n));
      if (r.dangerouslySetInnerHTML != null) {
        if (r.children != null)
          throw Error(b(60));
        if (typeof r.dangerouslySetInnerHTML != "object" || !("__html" in r.dangerouslySetInnerHTML))
          throw Error(b(61));
      }
      if (r.style != null && typeof r.style != "object")
        throw Error(b(62));
    }
  }
  function Cn(n, r) {
    if (n.indexOf("-") === -1)
      return typeof r.is == "string";
    switch (n) {
      case "annotation-xml":
      case "color-profile":
      case "font-face":
      case "font-face-src":
      case "font-face-uri":
      case "font-face-format":
      case "font-face-name":
      case "missing-glyph":
        return !1;
      default:
        return !0;
    }
  }
  var wr = null;
  function tn(n) {
    return n = n.target || n.srcElement || window, n.correspondingUseElement && (n = n.correspondingUseElement), n.nodeType === 3 ? n.parentNode : n;
  }
  var Mr = null, Xt = null, Kt = null;
  function ai(n) {
    if (n = ms(n)) {
      if (typeof Mr != "function")
        throw Error(b(280));
      var r = n.stateNode;
      r && (r = qe(r), Mr(n.stateNode, n.type, r));
    }
  }
  function La(n) {
    Xt ? Kt ? Kt.push(n) : Kt = [n] : Xt = n;
  }
  function pl() {
    if (Xt) {
      var n = Xt, r = Kt;
      if (Kt = Xt = null, ai(n), r)
        for (n = 0; n < r.length; n++)
          ai(r[n]);
    }
  }
  function Kl(n, r) {
    return n(r);
  }
  function Po() {
  }
  var Ui = !1;
  function vl(n, r, l) {
    if (Ui)
      return n(r, l);
    Ui = !0;
    try {
      return Kl(n, r, l);
    } finally {
      Ui = !1, (Xt !== null || Kt !== null) && (Po(), pl());
    }
  }
  function Sa(n, r) {
    var l = n.stateNode;
    if (l === null)
      return null;
    var u = qe(l);
    if (u === null)
      return null;
    l = u[r];
    e:
      switch (r) {
        case "onClick":
        case "onClickCapture":
        case "onDoubleClick":
        case "onDoubleClickCapture":
        case "onMouseDown":
        case "onMouseDownCapture":
        case "onMouseMove":
        case "onMouseMoveCapture":
        case "onMouseUp":
        case "onMouseUpCapture":
        case "onMouseEnter":
          (u = !u.disabled) || (n = n.type, u = !(n === "button" || n === "input" || n === "select" || n === "textarea")), n = !u;
          break e;
        default:
          n = !1;
      }
    if (n)
      return null;
    if (l && typeof l != "function")
      throw Error(b(231, r, typeof l));
    return l;
  }
  var yi = !1;
  if (ce)
    try {
      var xa = {};
      Object.defineProperty(xa, "passive", { get: function() {
        yi = !0;
      } }), window.addEventListener("test", xa, xa), window.removeEventListener("test", xa, xa);
    } catch {
      yi = !1;
    }
  function ii(n, r, l, u, c, d, m, E, k) {
    var H = Array.prototype.slice.call(arguments, 3);
    try {
      r.apply(l, H);
    } catch (re) {
      this.onError(re);
    }
  }
  var Lr = !1, ba = null, gi = !1, Si = null, T = { onError: function(n) {
    Lr = !0, ba = n;
  } };
  function ee(n, r, l, u, c, d, m, E, k) {
    Lr = !1, ba = null, ii.apply(T, arguments);
  }
  function ie(n, r, l, u, c, d, m, E, k) {
    if (ee.apply(this, arguments), Lr) {
      if (Lr) {
        var H = ba;
        Lr = !1, ba = null;
      } else
        throw Error(b(198));
      gi || (gi = !0, Si = H);
    }
  }
  function Pe(n) {
    var r = n, l = n;
    if (n.alternate)
      for (; r.return; )
        r = r.return;
    else {
      n = r;
      do
        r = n, r.flags & 4098 && (l = r.return), n = r.return;
      while (n);
    }
    return r.tag === 3 ? l : null;
  }
  function Tt(n) {
    if (n.tag === 13) {
      var r = n.memoizedState;
      if (r === null && (n = n.alternate, n !== null && (r = n.memoizedState)), r !== null)
        return r.dehydrated;
    }
    return null;
  }
  function jt(n) {
    if (Pe(n) !== n)
      throw Error(b(188));
  }
  function Ze(n) {
    var r = n.alternate;
    if (!r) {
      if (r = Pe(n), r === null)
        throw Error(b(188));
      return r !== n ? null : n;
    }
    for (var l = n, u = r; ; ) {
      var c = l.return;
      if (c === null)
        break;
      var d = c.alternate;
      if (d === null) {
        if (u = c.return, u !== null) {
          l = u;
          continue;
        }
        break;
      }
      if (c.child === d.child) {
        for (d = c.child; d; ) {
          if (d === l)
            return jt(c), n;
          if (d === u)
            return jt(c), r;
          d = d.sibling;
        }
        throw Error(b(188));
      }
      if (l.return !== u.return)
        l = c, u = d;
      else {
        for (var m = !1, E = c.child; E; ) {
          if (E === l) {
            m = !0, l = c, u = d;
            break;
          }
          if (E === u) {
            m = !0, u = c, l = d;
            break;
          }
          E = E.sibling;
        }
        if (!m) {
          for (E = d.child; E; ) {
            if (E === l) {
              m = !0, l = d, u = c;
              break;
            }
            if (E === u) {
              m = !0, u = d, l = c;
              break;
            }
            E = E.sibling;
          }
          if (!m)
            throw Error(b(189));
        }
      }
      if (l.alternate !== u)
        throw Error(b(190));
    }
    if (l.tag !== 3)
      throw Error(b(188));
    return l.stateNode.current === l ? n : r;
  }
  function Ct(n) {
    return n = Ze(n), n !== null ? Pn(n) : null;
  }
  function Pn(n) {
    if (n.tag === 5 || n.tag === 6)
      return n;
    for (n = n.child; n !== null; ) {
      var r = Pn(n);
      if (r !== null)
        return r;
      n = n.sibling;
    }
    return null;
  }
  var ln = w.unstable_scheduleCallback, dn = w.unstable_cancelCallback, Rr = w.unstable_shouldYield, xi = w.unstable_requestPaint, Vt = w.unstable_now, tr = w.unstable_getCurrentPriorityLevel, jr = w.unstable_ImmediatePriority, Et = w.unstable_UserBlockingPriority, ja = w.unstable_NormalPriority, hl = w.unstable_LowPriority, Vo = w.unstable_IdlePriority, ml = null, Jr = null;
  function Zu(n) {
    if (Jr && typeof Jr.onCommitFiberRoot == "function")
      try {
        Jr.onCommitFiberRoot(ml, n, void 0, (n.current.flags & 128) === 128);
      } catch {
      }
  }
  var zr = Math.clz32 ? Math.clz32 : cc, es = Math.log, ts = Math.LN2;
  function cc(n) {
    return n >>>= 0, n === 0 ? 32 : 31 - (es(n) / ts | 0) | 0;
  }
  var Bo = 64, yl = 4194304;
  function li(n) {
    switch (n & -n) {
      case 1:
        return 1;
      case 2:
        return 2;
      case 4:
        return 4;
      case 8:
        return 8;
      case 16:
        return 16;
      case 32:
        return 32;
      case 64:
      case 128:
      case 256:
      case 512:
      case 1024:
      case 2048:
      case 4096:
      case 8192:
      case 16384:
      case 32768:
      case 65536:
      case 131072:
      case 262144:
      case 524288:
      case 1048576:
      case 2097152:
        return n & 4194240;
      case 4194304:
      case 8388608:
      case 16777216:
      case 33554432:
      case 67108864:
        return n & 130023424;
      case 134217728:
        return 134217728;
      case 268435456:
        return 268435456;
      case 536870912:
        return 536870912;
      case 1073741824:
        return 1073741824;
      default:
        return n;
    }
  }
  function Ar(n, r) {
    var l = n.pendingLanes;
    if (l === 0)
      return 0;
    var u = 0, c = n.suspendedLanes, d = n.pingedLanes, m = l & 268435455;
    if (m !== 0) {
      var E = m & ~c;
      E !== 0 ? u = li(E) : (d &= m, d !== 0 && (u = li(d)));
    } else
      m = l & ~c, m !== 0 ? u = li(m) : d !== 0 && (u = li(d));
    if (u === 0)
      return 0;
    if (r !== 0 && r !== u && !(r & c) && (c = u & -u, d = r & -r, c >= d || c === 16 && (d & 4194240) !== 0))
      return r;
    if (u & 4 && (u |= l & 16), r = n.entangledLanes, r !== 0)
      for (n = n.entanglements, r &= u; 0 < r; )
        l = 31 - zr(r), c = 1 << l, u |= n[l], r &= ~c;
    return u;
  }
  function gl(n, r) {
    switch (n) {
      case 1:
      case 2:
      case 4:
        return r + 250;
      case 8:
      case 16:
      case 32:
      case 64:
      case 128:
      case 256:
      case 512:
      case 1024:
      case 2048:
      case 4096:
      case 8192:
      case 16384:
      case 32768:
      case 65536:
      case 131072:
      case 262144:
      case 524288:
      case 1048576:
      case 2097152:
        return r + 5e3;
      case 4194304:
      case 8388608:
      case 16777216:
      case 33554432:
      case 67108864:
        return -1;
      case 134217728:
      case 268435456:
      case 536870912:
      case 1073741824:
        return -1;
      default:
        return -1;
    }
  }
  function Sl(n, r) {
    for (var l = n.suspendedLanes, u = n.pingedLanes, c = n.expirationTimes, d = n.pendingLanes; 0 < d; ) {
      var m = 31 - zr(d), E = 1 << m, k = c[m];
      k === -1 ? (!(E & l) || E & u) && (c[m] = gl(E, r)) : k <= r && (n.expiredLanes |= E), d &= ~E;
    }
  }
  function xl(n) {
    return n = n.pendingLanes & -1073741825, n !== 0 ? n : n & 1073741824 ? 1073741824 : 0;
  }
  function $o() {
    var n = Bo;
    return Bo <<= 1, !(Bo & 4194240) && (Bo = 64), n;
  }
  function Io(n) {
    for (var r = [], l = 0; 31 > l; l++)
      r.push(n);
    return r;
  }
  function Fi(n, r, l) {
    n.pendingLanes |= r, r !== 536870912 && (n.suspendedLanes = 0, n.pingedLanes = 0), n = n.eventTimes, r = 31 - zr(r), n[r] = l;
  }
  function id(n, r) {
    var l = n.pendingLanes & ~r;
    n.pendingLanes = r, n.suspendedLanes = 0, n.pingedLanes = 0, n.expiredLanes &= r, n.mutableReadLanes &= r, n.entangledLanes &= r, r = n.entanglements;
    var u = n.eventTimes;
    for (n = n.expirationTimes; 0 < l; ) {
      var c = 31 - zr(l), d = 1 << c;
      r[c] = 0, u[c] = -1, n[c] = -1, l &= ~d;
    }
  }
  function bi(n, r) {
    var l = n.entangledLanes |= r;
    for (n = n.entanglements; l; ) {
      var u = 31 - zr(l), c = 1 << u;
      c & r | n[u] & r && (n[u] |= r), l &= ~c;
    }
  }
  var Bt = 0;
  function Yo(n) {
    return n &= -n, 1 < n ? 4 < n ? n & 268435455 ? 16 : 536870912 : 4 : 1;
  }
  var Jl, Wo, zt, Qo, Go, dt = !1, Zl = [], En = null, Zr = null, Ur = null, bl = /* @__PURE__ */ new Map(), kn = /* @__PURE__ */ new Map(), Jt = [], fc = "mousedown mouseup touchcancel touchend touchstart auxclick dblclick pointercancel pointerdown pointerup dragend dragstart drop compositionend compositionstart keydown keypress keyup input textInput copy cut paste click change contextmenu reset submit".split(" ");
  function ea(n, r) {
    switch (n) {
      case "focusin":
      case "focusout":
        En = null;
        break;
      case "dragenter":
      case "dragleave":
        Zr = null;
        break;
      case "mouseover":
      case "mouseout":
        Ur = null;
        break;
      case "pointerover":
      case "pointerout":
        bl.delete(r.pointerId);
        break;
      case "gotpointercapture":
      case "lostpointercapture":
        kn.delete(r.pointerId);
    }
  }
  function nr(n, r, l, u, c, d) {
    return n === null || n.nativeEvent !== d ? (n = { blockedOn: r, domEventName: l, eventSystemFlags: u, nativeEvent: d, targetContainers: [c] }, r !== null && (r = ms(r), r !== null && Wo(r)), n) : (n.eventSystemFlags |= u, r = n.targetContainers, c !== null && r.indexOf(c) === -1 && r.push(c), n);
  }
  function Ci(n, r, l, u, c) {
    switch (r) {
      case "focusin":
        return En = nr(En, n, r, l, u, c), !0;
      case "dragenter":
        return Zr = nr(Zr, n, r, l, u, c), !0;
      case "mouseover":
        return Ur = nr(Ur, n, r, l, u, c), !0;
      case "pointerover":
        var d = c.pointerId;
        return bl.set(d, nr(bl.get(d) || null, n, r, l, u, c)), !0;
      case "gotpointercapture":
        return d = c.pointerId, kn.set(d, nr(kn.get(d) || null, n, r, l, u, c)), !0;
    }
    return !1;
  }
  function dc(n) {
    var r = Fa(n.target);
    if (r !== null) {
      var l = Pe(r);
      if (l !== null) {
        if (r = l.tag, r === 13) {
          if (r = Tt(l), r !== null) {
            n.blockedOn = r, Go(n.priority, function() {
              zt(l);
            });
            return;
          }
        } else if (r === 3 && l.stateNode.current.memoizedState.isDehydrated) {
          n.blockedOn = l.tag === 3 ? l.stateNode.containerInfo : null;
          return;
        }
      }
    }
    n.blockedOn = null;
  }
  function Hi(n) {
    if (n.blockedOn !== null)
      return !1;
    for (var r = n.targetContainers; 0 < r.length; ) {
      var l = Xo(n.domEventName, n.eventSystemFlags, r[0], n.nativeEvent);
      if (l === null) {
        l = n.nativeEvent;
        var u = new l.constructor(l.type, l);
        wr = u, l.target.dispatchEvent(u), wr = null;
      } else
        return r = ms(l), r !== null && Wo(r), n.blockedOn = l, !1;
      r.shift();
    }
    return !0;
  }
  function Cl(n, r, l) {
    Hi(n) && l.delete(r);
  }
  function pc() {
    dt = !1, En !== null && Hi(En) && (En = null), Zr !== null && Hi(Zr) && (Zr = null), Ur !== null && Hi(Ur) && (Ur = null), bl.forEach(Cl), kn.forEach(Cl);
  }
  function za(n, r) {
    n.blockedOn === r && (n.blockedOn = null, dt || (dt = !0, w.unstable_scheduleCallback(w.unstable_NormalPriority, pc)));
  }
  function El(n) {
    function r(c) {
      return za(c, n);
    }
    if (0 < Zl.length) {
      za(Zl[0], n);
      for (var l = 1; l < Zl.length; l++) {
        var u = Zl[l];
        u.blockedOn === n && (u.blockedOn = null);
      }
    }
    for (En !== null && za(En, n), Zr !== null && za(Zr, n), Ur !== null && za(Ur, n), bl.forEach(r), kn.forEach(r), l = 0; l < Jt.length; l++)
      u = Jt[l], u.blockedOn === n && (u.blockedOn = null);
    for (; 0 < Jt.length && (l = Jt[0], l.blockedOn === null); )
      dc(l), l.blockedOn === null && Jt.shift();
  }
  var Pi = ct.ReactCurrentBatchConfig, Aa = !0;
  function qo(n, r, l, u) {
    var c = Bt, d = Pi.transition;
    Pi.transition = null;
    try {
      Bt = 1, Rl(n, r, l, u);
    } finally {
      Bt = c, Pi.transition = d;
    }
  }
  function wl(n, r, l, u) {
    var c = Bt, d = Pi.transition;
    Pi.transition = null;
    try {
      Bt = 4, Rl(n, r, l, u);
    } finally {
      Bt = c, Pi.transition = d;
    }
  }
  function Rl(n, r, l, u) {
    if (Aa) {
      var c = Xo(n, r, l, u);
      if (c === null)
        Cc(n, r, u, eo, l), ea(n, u);
      else if (Ci(c, n, r, l, u))
        u.stopPropagation();
      else if (ea(n, u), r & 4 && -1 < fc.indexOf(n)) {
        for (; c !== null; ) {
          var d = ms(c);
          if (d !== null && Jl(d), d = Xo(n, r, l, u), d === null && Cc(n, r, u, eo, l), d === c)
            break;
          c = d;
        }
        c !== null && u.stopPropagation();
      } else
        Cc(n, r, u, null, l);
    }
  }
  var eo = null;
  function Xo(n, r, l, u) {
    if (eo = null, n = tn(u), n = Fa(n), n !== null)
      if (r = Pe(n), r === null)
        n = null;
      else if (l = r.tag, l === 13) {
        if (n = Tt(r), n !== null)
          return n;
        n = null;
      } else if (l === 3) {
        if (r.stateNode.current.memoizedState.isDehydrated)
          return r.tag === 3 ? r.stateNode.containerInfo : null;
        n = null;
      } else
        r !== n && (n = null);
    return eo = n, null;
  }
  function ns(n) {
    switch (n) {
      case "cancel":
      case "click":
      case "close":
      case "contextmenu":
      case "copy":
      case "cut":
      case "auxclick":
      case "dblclick":
      case "dragend":
      case "dragstart":
      case "drop":
      case "focusin":
      case "focusout":
      case "input":
      case "invalid":
      case "keydown":
      case "keypress":
      case "keyup":
      case "mousedown":
      case "mouseup":
      case "paste":
      case "pause":
      case "play":
      case "pointercancel":
      case "pointerdown":
      case "pointerup":
      case "ratechange":
      case "reset":
      case "resize":
      case "seeked":
      case "submit":
      case "touchcancel":
      case "touchend":
      case "touchstart":
      case "volumechange":
      case "change":
      case "selectionchange":
      case "textInput":
      case "compositionstart":
      case "compositionend":
      case "compositionupdate":
      case "beforeblur":
      case "afterblur":
      case "beforeinput":
      case "blur":
      case "fullscreenchange":
      case "focus":
      case "hashchange":
      case "popstate":
      case "select":
      case "selectstart":
        return 1;
      case "drag":
      case "dragenter":
      case "dragexit":
      case "dragleave":
      case "dragover":
      case "mousemove":
      case "mouseout":
      case "mouseover":
      case "pointermove":
      case "pointerout":
      case "pointerover":
      case "scroll":
      case "toggle":
      case "touchmove":
      case "wheel":
      case "mouseenter":
      case "mouseleave":
      case "pointerenter":
      case "pointerleave":
        return 4;
      case "message":
        switch (tr()) {
          case jr:
            return 1;
          case Et:
            return 4;
          case ja:
          case hl:
            return 16;
          case Vo:
            return 536870912;
          default:
            return 16;
        }
      default:
        return 16;
    }
  }
  var oi = null, h = null, R = null;
  function F() {
    if (R)
      return R;
    var n, r = h, l = r.length, u, c = "value" in oi ? oi.value : oi.textContent, d = c.length;
    for (n = 0; n < l && r[n] === c[n]; n++)
      ;
    var m = l - n;
    for (u = 1; u <= m && r[l - u] === c[d - u]; u++)
      ;
    return R = c.slice(n, 1 < u ? 1 - u : void 0);
  }
  function Y(n) {
    var r = n.keyCode;
    return "charCode" in n ? (n = n.charCode, n === 0 && r === 13 && (n = 13)) : n = r, n === 10 && (n = 13), 32 <= n || n === 13 ? n : 0;
  }
  function ue() {
    return !0;
  }
  function et() {
    return !1;
  }
  function me(n) {
    function r(l, u, c, d, m) {
      this._reactName = l, this._targetInst = c, this.type = u, this.nativeEvent = d, this.target = m, this.currentTarget = null;
      for (var E in n)
        n.hasOwnProperty(E) && (l = n[E], this[E] = l ? l(d) : d[E]);
      return this.isDefaultPrevented = (d.defaultPrevented != null ? d.defaultPrevented : d.returnValue === !1) ? ue : et, this.isPropagationStopped = et, this;
    }
    return pe(r.prototype, { preventDefault: function() {
      this.defaultPrevented = !0;
      var l = this.nativeEvent;
      l && (l.preventDefault ? l.preventDefault() : typeof l.returnValue != "unknown" && (l.returnValue = !1), this.isDefaultPrevented = ue);
    }, stopPropagation: function() {
      var l = this.nativeEvent;
      l && (l.stopPropagation ? l.stopPropagation() : typeof l.cancelBubble != "unknown" && (l.cancelBubble = !0), this.isPropagationStopped = ue);
    }, persist: function() {
    }, isPersistent: ue }), r;
  }
  var Je = { eventPhase: 0, bubbles: 0, cancelable: 0, timeStamp: function(n) {
    return n.timeStamp || Date.now();
  }, defaultPrevented: 0, isTrusted: 0 }, kt = me(Je), Pt = pe({}, Je, { view: 0, detail: 0 }), on = me(Pt), nn, un, cn, At = pe({}, Pt, { screenX: 0, screenY: 0, clientX: 0, clientY: 0, pageX: 0, pageY: 0, ctrlKey: 0, shiftKey: 0, altKey: 0, metaKey: 0, getModifierState: cd, button: 0, buttons: 0, relatedTarget: function(n) {
    return n.relatedTarget === void 0 ? n.fromElement === n.srcElement ? n.toElement : n.fromElement : n.relatedTarget;
  }, movementX: function(n) {
    return "movementX" in n ? n.movementX : (n !== cn && (cn && n.type === "mousemove" ? (nn = n.screenX - cn.screenX, un = n.screenY - cn.screenY) : un = nn = 0, cn = n), nn);
  }, movementY: function(n) {
    return "movementY" in n ? n.movementY : un;
  } }), Vi = me(At), Ko = pe({}, At, { dataTransfer: 0 }), rs = me(Ko), ld = pe({}, Pt, { relatedTarget: 0 }), ui = me(ld), as = pe({}, Je, { animationName: 0, elapsedTime: 0, pseudoElement: 0 }), is = me(as), od = pe({}, Je, { clipboardData: function(n) {
    return "clipboardData" in n ? n.clipboardData : window.clipboardData;
  } }), fy = me(od), dy = pe({}, Je, { data: 0 }), ud = me(dy), sd = {
    Esc: "Escape",
    Spacebar: " ",
    Left: "ArrowLeft",
    Up: "ArrowUp",
    Right: "ArrowRight",
    Down: "ArrowDown",
    Del: "Delete",
    Win: "OS",
    Menu: "ContextMenu",
    Apps: "ContextMenu",
    Scroll: "ScrollLock",
    MozPrintableKey: "Unidentified"
  }, mv = {
    8: "Backspace",
    9: "Tab",
    12: "Clear",
    13: "Enter",
    16: "Shift",
    17: "Control",
    18: "Alt",
    19: "Pause",
    20: "CapsLock",
    27: "Escape",
    32: " ",
    33: "PageUp",
    34: "PageDown",
    35: "End",
    36: "Home",
    37: "ArrowLeft",
    38: "ArrowUp",
    39: "ArrowRight",
    40: "ArrowDown",
    45: "Insert",
    46: "Delete",
    112: "F1",
    113: "F2",
    114: "F3",
    115: "F4",
    116: "F5",
    117: "F6",
    118: "F7",
    119: "F8",
    120: "F9",
    121: "F10",
    122: "F11",
    123: "F12",
    144: "NumLock",
    145: "ScrollLock",
    224: "Meta"
  }, yv = { Alt: "altKey", Control: "ctrlKey", Meta: "metaKey", Shift: "shiftKey" };
  function gv(n) {
    var r = this.nativeEvent;
    return r.getModifierState ? r.getModifierState(n) : (n = yv[n]) ? !!r[n] : !1;
  }
  function cd() {
    return gv;
  }
  var Bi = pe({}, Pt, { key: function(n) {
    if (n.key) {
      var r = sd[n.key] || n.key;
      if (r !== "Unidentified")
        return r;
    }
    return n.type === "keypress" ? (n = Y(n), n === 13 ? "Enter" : String.fromCharCode(n)) : n.type === "keydown" || n.type === "keyup" ? mv[n.keyCode] || "Unidentified" : "";
  }, code: 0, location: 0, ctrlKey: 0, shiftKey: 0, altKey: 0, metaKey: 0, repeat: 0, locale: 0, getModifierState: cd, charCode: function(n) {
    return n.type === "keypress" ? Y(n) : 0;
  }, keyCode: function(n) {
    return n.type === "keydown" || n.type === "keyup" ? n.keyCode : 0;
  }, which: function(n) {
    return n.type === "keypress" ? Y(n) : n.type === "keydown" || n.type === "keyup" ? n.keyCode : 0;
  } }), py = me(Bi), fd = pe({}, At, { pointerId: 0, width: 0, height: 0, pressure: 0, tangentialPressure: 0, tiltX: 0, tiltY: 0, twist: 0, pointerType: 0, isPrimary: 0 }), vc = me(fd), dd = pe({}, Pt, { touches: 0, targetTouches: 0, changedTouches: 0, altKey: 0, metaKey: 0, ctrlKey: 0, shiftKey: 0, getModifierState: cd }), vy = me(dd), hc = pe({}, Je, { propertyName: 0, elapsedTime: 0, pseudoElement: 0 }), Sv = me(hc), ta = pe({}, At, {
    deltaX: function(n) {
      return "deltaX" in n ? n.deltaX : "wheelDeltaX" in n ? -n.wheelDeltaX : 0;
    },
    deltaY: function(n) {
      return "deltaY" in n ? n.deltaY : "wheelDeltaY" in n ? -n.wheelDeltaY : "wheelDelta" in n ? -n.wheelDelta : 0;
    },
    deltaZ: 0,
    deltaMode: 0
  }), $i = me(ta), Vn = [9, 13, 27, 32], si = ce && "CompositionEvent" in window, to = null;
  ce && "documentMode" in document && (to = document.documentMode);
  var mc = ce && "TextEvent" in window && !to, xv = ce && (!si || to && 8 < to && 11 >= to), Jo = String.fromCharCode(32), bv = !1;
  function Cv(n, r) {
    switch (n) {
      case "keyup":
        return Vn.indexOf(r.keyCode) !== -1;
      case "keydown":
        return r.keyCode !== 229;
      case "keypress":
      case "mousedown":
      case "focusout":
        return !0;
      default:
        return !1;
    }
  }
  function yc(n) {
    return n = n.detail, typeof n == "object" && "data" in n ? n.data : null;
  }
  var Zo = !1;
  function hy(n, r) {
    switch (n) {
      case "compositionend":
        return yc(r);
      case "keypress":
        return r.which !== 32 ? null : (bv = !0, Jo);
      case "textInput":
        return n = r.data, n === Jo && bv ? null : n;
      default:
        return null;
    }
  }
  function my(n, r) {
    if (Zo)
      return n === "compositionend" || !si && Cv(n, r) ? (n = F(), R = h = oi = null, Zo = !1, n) : null;
    switch (n) {
      case "paste":
        return null;
      case "keypress":
        if (!(r.ctrlKey || r.altKey || r.metaKey) || r.ctrlKey && r.altKey) {
          if (r.char && 1 < r.char.length)
            return r.char;
          if (r.which)
            return String.fromCharCode(r.which);
        }
        return null;
      case "compositionend":
        return xv && r.locale !== "ko" ? null : r.data;
      default:
        return null;
    }
  }
  var Ev = { color: !0, date: !0, datetime: !0, "datetime-local": !0, email: !0, month: !0, number: !0, password: !0, range: !0, search: !0, tel: !0, text: !0, time: !0, url: !0, week: !0 };
  function wv(n) {
    var r = n && n.nodeName && n.nodeName.toLowerCase();
    return r === "input" ? !!Ev[n.type] : r === "textarea";
  }
  function Rv(n, r, l, u) {
    La(u), r = ps(r, "onChange"), 0 < r.length && (l = new kt("onChange", "change", null, l, u), n.push({ event: l, listeners: r }));
  }
  var ls = null, eu = null;
  function tu(n) {
    bc(n, 0);
  }
  function nu(n) {
    var r = au(n);
    if (Yn(r))
      return n;
  }
  function Tv(n, r) {
    if (n === "change")
      return r;
  }
  var pd = !1;
  if (ce) {
    var vd;
    if (ce) {
      var hd = "oninput" in document;
      if (!hd) {
        var kv = document.createElement("div");
        kv.setAttribute("oninput", "return;"), hd = typeof kv.oninput == "function";
      }
      vd = hd;
    } else
      vd = !1;
    pd = vd && (!document.documentMode || 9 < document.documentMode);
  }
  function _v() {
    ls && (ls.detachEvent("onpropertychange", Dv), eu = ls = null);
  }
  function Dv(n) {
    if (n.propertyName === "value" && nu(eu)) {
      var r = [];
      Rv(r, eu, n, tn(n)), vl(tu, r);
    }
  }
  function yy(n, r, l) {
    n === "focusin" ? (_v(), ls = r, eu = l, ls.attachEvent("onpropertychange", Dv)) : n === "focusout" && _v();
  }
  function gy(n) {
    if (n === "selectionchange" || n === "keyup" || n === "keydown")
      return nu(eu);
  }
  function Sy(n, r) {
    if (n === "click")
      return nu(r);
  }
  function Nv(n, r) {
    if (n === "input" || n === "change")
      return nu(r);
  }
  function xy(n, r) {
    return n === r && (n !== 0 || 1 / n === 1 / r) || n !== n && r !== r;
  }
  var Ua = typeof Object.is == "function" ? Object.is : xy;
  function os(n, r) {
    if (Ua(n, r))
      return !0;
    if (typeof n != "object" || n === null || typeof r != "object" || r === null)
      return !1;
    var l = Object.keys(n), u = Object.keys(r);
    if (l.length !== u.length)
      return !1;
    for (u = 0; u < l.length; u++) {
      var c = l[u];
      if (!B.call(r, c) || !Ua(n[c], r[c]))
        return !1;
    }
    return !0;
  }
  function Ov(n) {
    for (; n && n.firstChild; )
      n = n.firstChild;
    return n;
  }
  function Mv(n, r) {
    var l = Ov(n);
    n = 0;
    for (var u; l; ) {
      if (l.nodeType === 3) {
        if (u = n + l.textContent.length, n <= r && u >= r)
          return { node: l, offset: r - n };
        n = u;
      }
      e: {
        for (; l; ) {
          if (l.nextSibling) {
            l = l.nextSibling;
            break e;
          }
          l = l.parentNode;
        }
        l = void 0;
      }
      l = Ov(l);
    }
  }
  function Lv(n, r) {
    return n && r ? n === r ? !0 : n && n.nodeType === 3 ? !1 : r && r.nodeType === 3 ? Lv(n, r.parentNode) : "contains" in n ? n.contains(r) : n.compareDocumentPosition ? !!(n.compareDocumentPosition(r) & 16) : !1 : !1;
  }
  function gc() {
    for (var n = window, r = xn(); r instanceof n.HTMLIFrameElement; ) {
      try {
        var l = typeof r.contentWindow.location.href == "string";
      } catch {
        l = !1;
      }
      if (l)
        n = r.contentWindow;
      else
        break;
      r = xn(n.document);
    }
    return r;
  }
  function Ii(n) {
    var r = n && n.nodeName && n.nodeName.toLowerCase();
    return r && (r === "input" && (n.type === "text" || n.type === "search" || n.type === "tel" || n.type === "url" || n.type === "password") || r === "textarea" || n.contentEditable === "true");
  }
  function Sc(n) {
    var r = gc(), l = n.focusedElem, u = n.selectionRange;
    if (r !== l && l && l.ownerDocument && Lv(l.ownerDocument.documentElement, l)) {
      if (u !== null && Ii(l)) {
        if (r = u.start, n = u.end, n === void 0 && (n = r), "selectionStart" in l)
          l.selectionStart = r, l.selectionEnd = Math.min(n, l.value.length);
        else if (n = (r = l.ownerDocument || document) && r.defaultView || window, n.getSelection) {
          n = n.getSelection();
          var c = l.textContent.length, d = Math.min(u.start, c);
          u = u.end === void 0 ? d : Math.min(u.end, c), !n.extend && d > u && (c = u, u = d, d = c), c = Mv(l, d);
          var m = Mv(
            l,
            u
          );
          c && m && (n.rangeCount !== 1 || n.anchorNode !== c.node || n.anchorOffset !== c.offset || n.focusNode !== m.node || n.focusOffset !== m.offset) && (r = r.createRange(), r.setStart(c.node, c.offset), n.removeAllRanges(), d > u ? (n.addRange(r), n.extend(m.node, m.offset)) : (r.setEnd(m.node, m.offset), n.addRange(r)));
        }
      }
      for (r = [], n = l; n = n.parentNode; )
        n.nodeType === 1 && r.push({ element: n, left: n.scrollLeft, top: n.scrollTop });
      for (typeof l.focus == "function" && l.focus(), l = 0; l < r.length; l++)
        n = r[l], n.element.scrollLeft = n.left, n.element.scrollTop = n.top;
    }
  }
  var jv = ce && "documentMode" in document && 11 >= document.documentMode, ci = null, md = null, us = null, yd = !1;
  function zv(n, r, l) {
    var u = l.window === l ? l.document : l.nodeType === 9 ? l : l.ownerDocument;
    yd || ci == null || ci !== xn(u) || (u = ci, "selectionStart" in u && Ii(u) ? u = { start: u.selectionStart, end: u.selectionEnd } : (u = (u.ownerDocument && u.ownerDocument.defaultView || window).getSelection(), u = { anchorNode: u.anchorNode, anchorOffset: u.anchorOffset, focusNode: u.focusNode, focusOffset: u.focusOffset }), us && os(us, u) || (us = u, u = ps(md, "onSelect"), 0 < u.length && (r = new kt("onSelect", "select", null, r, l), n.push({ event: r, listeners: u }), r.target = ci)));
  }
  function xc(n, r) {
    var l = {};
    return l[n.toLowerCase()] = r.toLowerCase(), l["Webkit" + n] = "webkit" + r, l["Moz" + n] = "moz" + r, l;
  }
  var no = { animationend: xc("Animation", "AnimationEnd"), animationiteration: xc("Animation", "AnimationIteration"), animationstart: xc("Animation", "AnimationStart"), transitionend: xc("Transition", "TransitionEnd") }, gd = {}, Sd = {};
  ce && (Sd = document.createElement("div").style, "AnimationEvent" in window || (delete no.animationend.animation, delete no.animationiteration.animation, delete no.animationstart.animation), "TransitionEvent" in window || delete no.transitionend.transition);
  function rr(n) {
    if (gd[n])
      return gd[n];
    if (!no[n])
      return n;
    var r = no[n], l;
    for (l in r)
      if (r.hasOwnProperty(l) && l in Sd)
        return gd[n] = r[l];
    return n;
  }
  var xd = rr("animationend"), Av = rr("animationiteration"), Uv = rr("animationstart"), Fv = rr("transitionend"), Hv = /* @__PURE__ */ new Map(), Pv = "abort auxClick cancel canPlay canPlayThrough click close contextMenu copy cut drag dragEnd dragEnter dragExit dragLeave dragOver dragStart drop durationChange emptied encrypted ended error gotPointerCapture input invalid keyDown keyPress keyUp load loadedData loadedMetadata loadStart lostPointerCapture mouseDown mouseMove mouseOut mouseOver mouseUp paste pause play playing pointerCancel pointerDown pointerMove pointerOut pointerOver pointerUp progress rateChange reset resize seeked seeking stalled submit suspend timeUpdate touchCancel touchEnd touchStart volumeChange scroll toggle touchMove waiting wheel".split(" ");
  function Yi(n, r) {
    Hv.set(n, r), W(r, [n]);
  }
  for (var ss = 0; ss < Pv.length; ss++) {
    var ro = Pv[ss], by = ro.toLowerCase(), cs = ro[0].toUpperCase() + ro.slice(1);
    Yi(by, "on" + cs);
  }
  Yi(xd, "onAnimationEnd"), Yi(Av, "onAnimationIteration"), Yi(Uv, "onAnimationStart"), Yi("dblclick", "onDoubleClick"), Yi("focusin", "onFocus"), Yi("focusout", "onBlur"), Yi(Fv, "onTransitionEnd"), y("onMouseEnter", ["mouseout", "mouseover"]), y("onMouseLeave", ["mouseout", "mouseover"]), y("onPointerEnter", ["pointerout", "pointerover"]), y("onPointerLeave", ["pointerout", "pointerover"]), W("onChange", "change click focusin focusout input keydown keyup selectionchange".split(" ")), W("onSelect", "focusout contextmenu dragend focusin keydown keyup mousedown mouseup selectionchange".split(" ")), W("onBeforeInput", ["compositionend", "keypress", "textInput", "paste"]), W("onCompositionEnd", "compositionend focusout keydown keypress keyup mousedown".split(" ")), W("onCompositionStart", "compositionstart focusout keydown keypress keyup mousedown".split(" ")), W("onCompositionUpdate", "compositionupdate focusout keydown keypress keyup mousedown".split(" "));
  var fs = "abort canplay canplaythrough durationchange emptied encrypted ended error loadeddata loadedmetadata loadstart pause play playing progress ratechange resize seeked seeking stalled suspend timeupdate volumechange waiting".split(" "), Cy = new Set("cancel close invalid load scroll toggle".split(" ").concat(fs));
  function Vv(n, r, l) {
    var u = n.type || "unknown-event";
    n.currentTarget = l, ie(u, r, void 0, n), n.currentTarget = null;
  }
  function bc(n, r) {
    r = (r & 4) !== 0;
    for (var l = 0; l < n.length; l++) {
      var u = n[l], c = u.event;
      u = u.listeners;
      e: {
        var d = void 0;
        if (r)
          for (var m = u.length - 1; 0 <= m; m--) {
            var E = u[m], k = E.instance, H = E.currentTarget;
            if (E = E.listener, k !== d && c.isPropagationStopped())
              break e;
            Vv(c, E, H), d = k;
          }
        else
          for (m = 0; m < u.length; m++) {
            if (E = u[m], k = E.instance, H = E.currentTarget, E = E.listener, k !== d && c.isPropagationStopped())
              break e;
            Vv(c, E, H), d = k;
          }
      }
    }
    if (gi)
      throw n = Si, gi = !1, Si = null, n;
  }
  function sn(n, r) {
    var l = r[kd];
    l === void 0 && (l = r[kd] = /* @__PURE__ */ new Set());
    var u = n + "__bubble";
    l.has(u) || (Bv(r, n, 2, !1), l.add(u));
  }
  function Tl(n, r, l) {
    var u = 0;
    r && (u |= 4), Bv(l, n, u, r);
  }
  var Wi = "_reactListening" + Math.random().toString(36).slice(2);
  function ru(n) {
    if (!n[Wi]) {
      n[Wi] = !0, U.forEach(function(l) {
        l !== "selectionchange" && (Cy.has(l) || Tl(l, !1, n), Tl(l, !0, n));
      });
      var r = n.nodeType === 9 ? n : n.ownerDocument;
      r === null || r[Wi] || (r[Wi] = !0, Tl("selectionchange", !1, r));
    }
  }
  function Bv(n, r, l, u) {
    switch (ns(r)) {
      case 1:
        var c = qo;
        break;
      case 4:
        c = wl;
        break;
      default:
        c = Rl;
    }
    l = c.bind(null, r, l, n), c = void 0, !yi || r !== "touchstart" && r !== "touchmove" && r !== "wheel" || (c = !0), u ? c !== void 0 ? n.addEventListener(r, l, { capture: !0, passive: c }) : n.addEventListener(r, l, !0) : c !== void 0 ? n.addEventListener(r, l, { passive: c }) : n.addEventListener(r, l, !1);
  }
  function Cc(n, r, l, u, c) {
    var d = u;
    if (!(r & 1) && !(r & 2) && u !== null)
      e:
        for (; ; ) {
          if (u === null)
            return;
          var m = u.tag;
          if (m === 3 || m === 4) {
            var E = u.stateNode.containerInfo;
            if (E === c || E.nodeType === 8 && E.parentNode === c)
              break;
            if (m === 4)
              for (m = u.return; m !== null; ) {
                var k = m.tag;
                if ((k === 3 || k === 4) && (k = m.stateNode.containerInfo, k === c || k.nodeType === 8 && k.parentNode === c))
                  return;
                m = m.return;
              }
            for (; E !== null; ) {
              if (m = Fa(E), m === null)
                return;
              if (k = m.tag, k === 5 || k === 6) {
                u = d = m;
                continue e;
              }
              E = E.parentNode;
            }
          }
          u = u.return;
        }
    vl(function() {
      var H = d, re = tn(l), ae = [];
      e: {
        var te = Hv.get(n);
        if (te !== void 0) {
          var Ce = kt, _e = n;
          switch (n) {
            case "keypress":
              if (Y(l) === 0)
                break e;
            case "keydown":
            case "keyup":
              Ce = py;
              break;
            case "focusin":
              _e = "focus", Ce = ui;
              break;
            case "focusout":
              _e = "blur", Ce = ui;
              break;
            case "beforeblur":
            case "afterblur":
              Ce = ui;
              break;
            case "click":
              if (l.button === 2)
                break e;
            case "auxclick":
            case "dblclick":
            case "mousedown":
            case "mousemove":
            case "mouseup":
            case "mouseout":
            case "mouseover":
            case "contextmenu":
              Ce = Vi;
              break;
            case "drag":
            case "dragend":
            case "dragenter":
            case "dragexit":
            case "dragleave":
            case "dragover":
            case "dragstart":
            case "drop":
              Ce = rs;
              break;
            case "touchcancel":
            case "touchend":
            case "touchmove":
            case "touchstart":
              Ce = vy;
              break;
            case xd:
            case Av:
            case Uv:
              Ce = is;
              break;
            case Fv:
              Ce = Sv;
              break;
            case "scroll":
              Ce = on;
              break;
            case "wheel":
              Ce = $i;
              break;
            case "copy":
            case "cut":
            case "paste":
              Ce = fy;
              break;
            case "gotpointercapture":
            case "lostpointercapture":
            case "pointercancel":
            case "pointerdown":
            case "pointermove":
            case "pointerout":
            case "pointerover":
            case "pointerup":
              Ce = vc;
          }
          var Le = (r & 4) !== 0, An = !Le && n === "scroll", M = Le ? te !== null ? te + "Capture" : null : te;
          Le = [];
          for (var D = H, z; D !== null; ) {
            z = D;
            var se = z.stateNode;
            if (z.tag === 5 && se !== null && (z = se, M !== null && (se = Sa(D, M), se != null && Le.push(ds(D, se, z)))), An)
              break;
            D = D.return;
          }
          0 < Le.length && (te = new Ce(te, _e, null, l, re), ae.push({ event: te, listeners: Le }));
        }
      }
      if (!(r & 7)) {
        e: {
          if (te = n === "mouseover" || n === "pointerover", Ce = n === "mouseout" || n === "pointerout", te && l !== wr && (_e = l.relatedTarget || l.fromElement) && (Fa(_e) || _e[Qi]))
            break e;
          if ((Ce || te) && (te = re.window === re ? re : (te = re.ownerDocument) ? te.defaultView || te.parentWindow : window, Ce ? (_e = l.relatedTarget || l.toElement, Ce = H, _e = _e ? Fa(_e) : null, _e !== null && (An = Pe(_e), _e !== An || _e.tag !== 5 && _e.tag !== 6) && (_e = null)) : (Ce = null, _e = H), Ce !== _e)) {
            if (Le = Vi, se = "onMouseLeave", M = "onMouseEnter", D = "mouse", (n === "pointerout" || n === "pointerover") && (Le = vc, se = "onPointerLeave", M = "onPointerEnter", D = "pointer"), An = Ce == null ? te : au(Ce), z = _e == null ? te : au(_e), te = new Le(se, D + "leave", Ce, l, re), te.target = An, te.relatedTarget = z, se = null, Fa(re) === H && (Le = new Le(M, D + "enter", _e, l, re), Le.target = z, Le.relatedTarget = An, se = Le), An = se, Ce && _e)
              t: {
                for (Le = Ce, M = _e, D = 0, z = Le; z; z = ao(z))
                  D++;
                for (z = 0, se = M; se; se = ao(se))
                  z++;
                for (; 0 < D - z; )
                  Le = ao(Le), D--;
                for (; 0 < z - D; )
                  M = ao(M), z--;
                for (; D--; ) {
                  if (Le === M || M !== null && Le === M.alternate)
                    break t;
                  Le = ao(Le), M = ao(M);
                }
                Le = null;
              }
            else
              Le = null;
            Ce !== null && bd(ae, te, Ce, Le, !1), _e !== null && An !== null && bd(ae, An, _e, Le, !0);
          }
        }
        e: {
          if (te = H ? au(H) : window, Ce = te.nodeName && te.nodeName.toLowerCase(), Ce === "select" || Ce === "input" && te.type === "file")
            var He = Tv;
          else if (wv(te))
            if (pd)
              He = Nv;
            else {
              He = gy;
              var tt = yy;
            }
          else
            (Ce = te.nodeName) && Ce.toLowerCase() === "input" && (te.type === "checkbox" || te.type === "radio") && (He = Sy);
          if (He && (He = He(n, H))) {
            Rv(ae, He, l, re);
            break e;
          }
          tt && tt(n, te, H), n === "focusout" && (tt = te._wrapperState) && tt.controlled && te.type === "number" && qr(te, "number", te.value);
        }
        switch (tt = H ? au(H) : window, n) {
          case "focusin":
            (wv(tt) || tt.contentEditable === "true") && (ci = tt, md = H, us = null);
            break;
          case "focusout":
            us = md = ci = null;
            break;
          case "mousedown":
            yd = !0;
            break;
          case "contextmenu":
          case "mouseup":
          case "dragend":
            yd = !1, zv(ae, l, re);
            break;
          case "selectionchange":
            if (jv)
              break;
          case "keydown":
          case "keyup":
            zv(ae, l, re);
        }
        var De;
        if (si)
          e: {
            switch (n) {
              case "compositionstart":
                var nt = "onCompositionStart";
                break e;
              case "compositionend":
                nt = "onCompositionEnd";
                break e;
              case "compositionupdate":
                nt = "onCompositionUpdate";
                break e;
            }
            nt = void 0;
          }
        else
          Zo ? Cv(n, l) && (nt = "onCompositionEnd") : n === "keydown" && l.keyCode === 229 && (nt = "onCompositionStart");
        nt && (xv && l.locale !== "ko" && (Zo || nt !== "onCompositionStart" ? nt === "onCompositionEnd" && Zo && (De = F()) : (oi = re, h = "value" in oi ? oi.value : oi.textContent, Zo = !0)), tt = ps(H, nt), 0 < tt.length && (nt = new ud(nt, n, null, l, re), ae.push({ event: nt, listeners: tt }), De ? nt.data = De : (De = yc(l), De !== null && (nt.data = De)))), (De = mc ? hy(n, l) : my(n, l)) && (H = ps(H, "onBeforeInput"), 0 < H.length && (re = new ud("onBeforeInput", "beforeinput", null, l, re), ae.push({ event: re, listeners: H }), re.data = De));
      }
      bc(ae, r);
    });
  }
  function ds(n, r, l) {
    return { instance: n, listener: r, currentTarget: l };
  }
  function ps(n, r) {
    for (var l = r + "Capture", u = []; n !== null; ) {
      var c = n, d = c.stateNode;
      c.tag === 5 && d !== null && (c = d, d = Sa(n, l), d != null && u.unshift(ds(n, d, c)), d = Sa(n, r), d != null && u.push(ds(n, d, c))), n = n.return;
    }
    return u;
  }
  function ao(n) {
    if (n === null)
      return null;
    do
      n = n.return;
    while (n && n.tag !== 5);
    return n || null;
  }
  function bd(n, r, l, u, c) {
    for (var d = r._reactName, m = []; l !== null && l !== u; ) {
      var E = l, k = E.alternate, H = E.stateNode;
      if (k !== null && k === u)
        break;
      E.tag === 5 && H !== null && (E = H, c ? (k = Sa(l, d), k != null && m.unshift(ds(l, k, E))) : c || (k = Sa(l, d), k != null && m.push(ds(l, k, E)))), l = l.return;
    }
    m.length !== 0 && n.push({ event: r, listeners: m });
  }
  var Cd = /\r\n?/g, Ey = /\u0000|\uFFFD/g;
  function Ed(n) {
    return (typeof n == "string" ? n : "" + n).replace(Cd, `
`).replace(Ey, "");
  }
  function Ec(n, r, l) {
    if (r = Ed(r), Ed(n) !== r && l)
      throw Error(b(425));
  }
  function wc() {
  }
  var wd = null, io = null;
  function vs(n, r) {
    return n === "textarea" || n === "noscript" || typeof r.children == "string" || typeof r.children == "number" || typeof r.dangerouslySetInnerHTML == "object" && r.dangerouslySetInnerHTML !== null && r.dangerouslySetInnerHTML.__html != null;
  }
  var lo = typeof setTimeout == "function" ? setTimeout : void 0, $v = typeof clearTimeout == "function" ? clearTimeout : void 0, Rd = typeof Promise == "function" ? Promise : void 0, Td = typeof queueMicrotask == "function" ? queueMicrotask : typeof Rd < "u" ? function(n) {
    return Rd.resolve(null).then(n).catch(wy);
  } : lo;
  function wy(n) {
    setTimeout(function() {
      throw n;
    });
  }
  function kl(n, r) {
    var l = r, u = 0;
    do {
      var c = l.nextSibling;
      if (n.removeChild(l), c && c.nodeType === 8)
        if (l = c.data, l === "/$") {
          if (u === 0) {
            n.removeChild(c), El(r);
            return;
          }
          u--;
        } else
          l !== "$" && l !== "$?" && l !== "$!" || u++;
      l = c;
    } while (l);
    El(r);
  }
  function fi(n) {
    for (; n != null; n = n.nextSibling) {
      var r = n.nodeType;
      if (r === 1 || r === 3)
        break;
      if (r === 8) {
        if (r = n.data, r === "$" || r === "$!" || r === "$?")
          break;
        if (r === "/$")
          return null;
      }
    }
    return n;
  }
  function hs(n) {
    n = n.previousSibling;
    for (var r = 0; n; ) {
      if (n.nodeType === 8) {
        var l = n.data;
        if (l === "$" || l === "$!" || l === "$?") {
          if (r === 0)
            return n;
          r--;
        } else
          l === "/$" && r++;
      }
      n = n.previousSibling;
    }
    return null;
  }
  var _l = Math.random().toString(36).slice(2), Ei = "__reactFiber$" + _l, oo = "__reactProps$" + _l, Qi = "__reactContainer$" + _l, kd = "__reactEvents$" + _l, Ry = "__reactListeners$" + _l, _d = "__reactHandles$" + _l;
  function Fa(n) {
    var r = n[Ei];
    if (r)
      return r;
    for (var l = n.parentNode; l; ) {
      if (r = l[Qi] || l[Ei]) {
        if (l = r.alternate, r.child !== null || l !== null && l.child !== null)
          for (n = hs(n); n !== null; ) {
            if (l = n[Ei])
              return l;
            n = hs(n);
          }
        return r;
      }
      n = l, l = n.parentNode;
    }
    return null;
  }
  function ms(n) {
    return n = n[Ei] || n[Qi], !n || n.tag !== 5 && n.tag !== 6 && n.tag !== 13 && n.tag !== 3 ? null : n;
  }
  function au(n) {
    if (n.tag === 5 || n.tag === 6)
      return n.stateNode;
    throw Error(b(33));
  }
  function qe(n) {
    return n[oo] || null;
  }
  var Dl = [], pn = -1;
  function xt(n) {
    return { current: n };
  }
  function Gt(n) {
    0 > pn || (n.current = Dl[pn], Dl[pn] = null, pn--);
  }
  function Zt(n, r) {
    pn++, Dl[pn] = n.current, n.current = r;
  }
  var wi = {}, ot = xt(wi), _n = xt(!1), na = wi;
  function Ha(n, r) {
    var l = n.type.contextTypes;
    if (!l)
      return wi;
    var u = n.stateNode;
    if (u && u.__reactInternalMemoizedUnmaskedChildContext === r)
      return u.__reactInternalMemoizedMaskedChildContext;
    var c = {}, d;
    for (d in l)
      c[d] = r[d];
    return u && (n = n.stateNode, n.__reactInternalMemoizedUnmaskedChildContext = r, n.__reactInternalMemoizedMaskedChildContext = c), c;
  }
  function yn(n) {
    return n = n.childContextTypes, n != null;
  }
  function Pa() {
    Gt(_n), Gt(ot);
  }
  function Nl(n, r, l) {
    if (ot.current !== wi)
      throw Error(b(168));
    Zt(ot, r), Zt(_n, l);
  }
  function ys(n, r, l) {
    var u = n.stateNode;
    if (r = r.childContextTypes, typeof u.getChildContext != "function")
      return l;
    u = u.getChildContext();
    for (var c in u)
      if (!(c in r))
        throw Error(b(108, Ge(n) || "Unknown", c));
    return pe({}, l, u);
  }
  function Rc(n) {
    return n = (n = n.stateNode) && n.__reactInternalMemoizedMergedChildContext || wi, na = ot.current, Zt(ot, n), Zt(_n, _n.current), !0;
  }
  function Iv(n, r, l) {
    var u = n.stateNode;
    if (!u)
      throw Error(b(169));
    l ? (n = ys(n, r, na), u.__reactInternalMemoizedMergedChildContext = n, Gt(_n), Gt(ot), Zt(ot, n)) : Gt(_n), Zt(_n, l);
  }
  var Ca = null, ar = !1, gs = !1;
  function Dd(n) {
    Ca === null ? Ca = [n] : Ca.push(n);
  }
  function Nd(n) {
    ar = !0, Dd(n);
  }
  function ra() {
    if (!gs && Ca !== null) {
      gs = !0;
      var n = 0, r = Bt;
      try {
        var l = Ca;
        for (Bt = 1; n < l.length; n++) {
          var u = l[n];
          do
            u = u(!0);
          while (u !== null);
        }
        Ca = null, ar = !1;
      } catch (c) {
        throw Ca !== null && (Ca = Ca.slice(n + 1)), ln(jr, ra), c;
      } finally {
        Bt = r, gs = !1;
      }
    }
    return null;
  }
  var Ol = [], aa = 0, uo = null, iu = 0, ia = [], Tr = 0, Va = null, cr = 1, Gi = "";
  function Ea(n, r) {
    Ol[aa++] = iu, Ol[aa++] = uo, uo = n, iu = r;
  }
  function Od(n, r, l) {
    ia[Tr++] = cr, ia[Tr++] = Gi, ia[Tr++] = Va, Va = n;
    var u = cr;
    n = Gi;
    var c = 32 - zr(u) - 1;
    u &= ~(1 << c), l += 1;
    var d = 32 - zr(r) + c;
    if (30 < d) {
      var m = c - c % 5;
      d = (u & (1 << m) - 1).toString(32), u >>= m, c -= m, cr = 1 << 32 - zr(r) + c | l << c | u, Gi = d + n;
    } else
      cr = 1 << d | l << c | u, Gi = n;
  }
  function Tc(n) {
    n.return !== null && (Ea(n, 1), Od(n, 1, 0));
  }
  function Md(n) {
    for (; n === uo; )
      uo = Ol[--aa], Ol[aa] = null, iu = Ol[--aa], Ol[aa] = null;
    for (; n === Va; )
      Va = ia[--Tr], ia[Tr] = null, Gi = ia[--Tr], ia[Tr] = null, cr = ia[--Tr], ia[Tr] = null;
  }
  var wa = null, la = null, vn = !1, Ba = null;
  function Ld(n, r) {
    var l = Xa(5, null, null, 0);
    l.elementType = "DELETED", l.stateNode = r, l.return = n, r = n.deletions, r === null ? (n.deletions = [l], n.flags |= 16) : r.push(l);
  }
  function Yv(n, r) {
    switch (n.tag) {
      case 5:
        var l = n.type;
        return r = r.nodeType !== 1 || l.toLowerCase() !== r.nodeName.toLowerCase() ? null : r, r !== null ? (n.stateNode = r, wa = n, la = fi(r.firstChild), !0) : !1;
      case 6:
        return r = n.pendingProps === "" || r.nodeType !== 3 ? null : r, r !== null ? (n.stateNode = r, wa = n, la = null, !0) : !1;
      case 13:
        return r = r.nodeType !== 8 ? null : r, r !== null ? (l = Va !== null ? { id: cr, overflow: Gi } : null, n.memoizedState = { dehydrated: r, treeContext: l, retryLane: 1073741824 }, l = Xa(18, null, null, 0), l.stateNode = r, l.return = n, n.child = l, wa = n, la = null, !0) : !1;
      default:
        return !1;
    }
  }
  function kc(n) {
    return (n.mode & 1) !== 0 && (n.flags & 128) === 0;
  }
  function _c(n) {
    if (vn) {
      var r = la;
      if (r) {
        var l = r;
        if (!Yv(n, r)) {
          if (kc(n))
            throw Error(b(418));
          r = fi(l.nextSibling);
          var u = wa;
          r && Yv(n, r) ? Ld(u, l) : (n.flags = n.flags & -4097 | 2, vn = !1, wa = n);
        }
      } else {
        if (kc(n))
          throw Error(b(418));
        n.flags = n.flags & -4097 | 2, vn = !1, wa = n;
      }
    }
  }
  function Wv(n) {
    for (n = n.return; n !== null && n.tag !== 5 && n.tag !== 3 && n.tag !== 13; )
      n = n.return;
    wa = n;
  }
  function Dc(n) {
    if (n !== wa)
      return !1;
    if (!vn)
      return Wv(n), vn = !0, !1;
    var r;
    if ((r = n.tag !== 3) && !(r = n.tag !== 5) && (r = n.type, r = r !== "head" && r !== "body" && !vs(n.type, n.memoizedProps)), r && (r = la)) {
      if (kc(n))
        throw Qv(), Error(b(418));
      for (; r; )
        Ld(n, r), r = fi(r.nextSibling);
    }
    if (Wv(n), n.tag === 13) {
      if (n = n.memoizedState, n = n !== null ? n.dehydrated : null, !n)
        throw Error(b(317));
      e: {
        for (n = n.nextSibling, r = 0; n; ) {
          if (n.nodeType === 8) {
            var l = n.data;
            if (l === "/$") {
              if (r === 0) {
                la = fi(n.nextSibling);
                break e;
              }
              r--;
            } else
              l !== "$" && l !== "$!" && l !== "$?" || r++;
          }
          n = n.nextSibling;
        }
        la = null;
      }
    } else
      la = wa ? fi(n.stateNode.nextSibling) : null;
    return !0;
  }
  function Qv() {
    for (var n = la; n; )
      n = fi(n.nextSibling);
  }
  function wn() {
    la = wa = null, vn = !1;
  }
  function jd(n) {
    Ba === null ? Ba = [n] : Ba.push(n);
  }
  var Nc = ct.ReactCurrentBatchConfig;
  function so(n, r, l) {
    if (n = l.ref, n !== null && typeof n != "function" && typeof n != "object") {
      if (l._owner) {
        if (l = l._owner, l) {
          if (l.tag !== 1)
            throw Error(b(309));
          var u = l.stateNode;
        }
        if (!u)
          throw Error(b(147, n));
        var c = u, d = "" + n;
        return r !== null && r.ref !== null && typeof r.ref == "function" && r.ref._stringRef === d ? r.ref : (r = function(m) {
          var E = c.refs;
          m === null ? delete E[d] : E[d] = m;
        }, r._stringRef = d, r);
      }
      if (typeof n != "string")
        throw Error(b(284));
      if (!l._owner)
        throw Error(b(290, n));
    }
    return n;
  }
  function Ri(n, r) {
    throw n = Object.prototype.toString.call(r), Error(b(31, n === "[object Object]" ? "object with keys {" + Object.keys(r).join(", ") + "}" : n));
  }
  function Gv(n) {
    var r = n._init;
    return r(n._payload);
  }
  function Oc(n) {
    function r(M, D) {
      if (n) {
        var z = M.deletions;
        z === null ? (M.deletions = [D], M.flags |= 16) : z.push(D);
      }
    }
    function l(M, D) {
      if (!n)
        return null;
      for (; D !== null; )
        r(M, D), D = D.sibling;
      return null;
    }
    function u(M, D) {
      for (M = /* @__PURE__ */ new Map(); D !== null; )
        D.key !== null ? M.set(D.key, D) : M.set(D.index, D), D = D.sibling;
      return M;
    }
    function c(M, D) {
      return M = Hl(M, D), M.index = 0, M.sibling = null, M;
    }
    function d(M, D, z) {
      return M.index = z, n ? (z = M.alternate, z !== null ? (z = z.index, z < D ? (M.flags |= 2, D) : z) : (M.flags |= 2, D)) : (M.flags |= 1048576, D);
    }
    function m(M) {
      return n && M.alternate === null && (M.flags |= 2), M;
    }
    function E(M, D, z, se) {
      return D === null || D.tag !== 6 ? (D = Sf(z, M.mode, se), D.return = M, D) : (D = c(D, z), D.return = M, D);
    }
    function k(M, D, z, se) {
      var He = z.type;
      return He === Ye ? re(M, D, z.props.children, se, z.key) : D !== null && (D.elementType === He || typeof He == "object" && He !== null && He.$$typeof === yt && Gv(He) === D.type) ? (se = c(D, z.props), se.ref = so(M, D, z), se.return = M, se) : (se = yf(z.type, z.key, z.props, null, M.mode, se), se.ref = so(M, D, z), se.return = M, se);
    }
    function H(M, D, z, se) {
      return D === null || D.tag !== 4 || D.stateNode.containerInfo !== z.containerInfo || D.stateNode.implementation !== z.implementation ? (D = As(z, M.mode, se), D.return = M, D) : (D = c(D, z.children || []), D.return = M, D);
    }
    function re(M, D, z, se, He) {
      return D === null || D.tag !== 7 ? (D = Ro(z, M.mode, se, He), D.return = M, D) : (D = c(D, z), D.return = M, D);
    }
    function ae(M, D, z) {
      if (typeof D == "string" && D !== "" || typeof D == "number")
        return D = Sf("" + D, M.mode, z), D.return = M, D;
      if (typeof D == "object" && D !== null) {
        switch (D.$$typeof) {
          case ke:
            return z = yf(D.type, D.key, D.props, null, M.mode, z), z.ref = so(M, null, D), z.return = M, z;
          case at:
            return D = As(D, M.mode, z), D.return = M, D;
          case yt:
            var se = D._init;
            return ae(M, se(D._payload), z);
        }
        if (er(D) || Ue(D))
          return D = Ro(D, M.mode, z, null), D.return = M, D;
        Ri(M, D);
      }
      return null;
    }
    function te(M, D, z, se) {
      var He = D !== null ? D.key : null;
      if (typeof z == "string" && z !== "" || typeof z == "number")
        return He !== null ? null : E(M, D, "" + z, se);
      if (typeof z == "object" && z !== null) {
        switch (z.$$typeof) {
          case ke:
            return z.key === He ? k(M, D, z, se) : null;
          case at:
            return z.key === He ? H(M, D, z, se) : null;
          case yt:
            return He = z._init, te(
              M,
              D,
              He(z._payload),
              se
            );
        }
        if (er(z) || Ue(z))
          return He !== null ? null : re(M, D, z, se, null);
        Ri(M, z);
      }
      return null;
    }
    function Ce(M, D, z, se, He) {
      if (typeof se == "string" && se !== "" || typeof se == "number")
        return M = M.get(z) || null, E(D, M, "" + se, He);
      if (typeof se == "object" && se !== null) {
        switch (se.$$typeof) {
          case ke:
            return M = M.get(se.key === null ? z : se.key) || null, k(D, M, se, He);
          case at:
            return M = M.get(se.key === null ? z : se.key) || null, H(D, M, se, He);
          case yt:
            var tt = se._init;
            return Ce(M, D, z, tt(se._payload), He);
        }
        if (er(se) || Ue(se))
          return M = M.get(z) || null, re(D, M, se, He, null);
        Ri(D, se);
      }
      return null;
    }
    function _e(M, D, z, se) {
      for (var He = null, tt = null, De = D, nt = D = 0, Kn = null; De !== null && nt < z.length; nt++) {
        De.index > nt ? (Kn = De, De = null) : Kn = De.sibling;
        var $t = te(M, De, z[nt], se);
        if ($t === null) {
          De === null && (De = Kn);
          break;
        }
        n && De && $t.alternate === null && r(M, De), D = d($t, D, nt), tt === null ? He = $t : tt.sibling = $t, tt = $t, De = Kn;
      }
      if (nt === z.length)
        return l(M, De), vn && Ea(M, nt), He;
      if (De === null) {
        for (; nt < z.length; nt++)
          De = ae(M, z[nt], se), De !== null && (D = d(De, D, nt), tt === null ? He = De : tt.sibling = De, tt = De);
        return vn && Ea(M, nt), He;
      }
      for (De = u(M, De); nt < z.length; nt++)
        Kn = Ce(De, M, nt, z[nt], se), Kn !== null && (n && Kn.alternate !== null && De.delete(Kn.key === null ? nt : Kn.key), D = d(Kn, D, nt), tt === null ? He = Kn : tt.sibling = Kn, tt = Kn);
      return n && De.forEach(function(tl) {
        return r(M, tl);
      }), vn && Ea(M, nt), He;
    }
    function Le(M, D, z, se) {
      var He = Ue(z);
      if (typeof He != "function")
        throw Error(b(150));
      if (z = He.call(z), z == null)
        throw Error(b(151));
      for (var tt = He = null, De = D, nt = D = 0, Kn = null, $t = z.next(); De !== null && !$t.done; nt++, $t = z.next()) {
        De.index > nt ? (Kn = De, De = null) : Kn = De.sibling;
        var tl = te(M, De, $t.value, se);
        if (tl === null) {
          De === null && (De = Kn);
          break;
        }
        n && De && tl.alternate === null && r(M, De), D = d(tl, D, nt), tt === null ? He = tl : tt.sibling = tl, tt = tl, De = Kn;
      }
      if ($t.done)
        return l(
          M,
          De
        ), vn && Ea(M, nt), He;
      if (De === null) {
        for (; !$t.done; nt++, $t = z.next())
          $t = ae(M, $t.value, se), $t !== null && (D = d($t, D, nt), tt === null ? He = $t : tt.sibling = $t, tt = $t);
        return vn && Ea(M, nt), He;
      }
      for (De = u(M, De); !$t.done; nt++, $t = z.next())
        $t = Ce(De, M, nt, $t.value, se), $t !== null && (n && $t.alternate !== null && De.delete($t.key === null ? nt : $t.key), D = d($t, D, nt), tt === null ? He = $t : tt.sibling = $t, tt = $t);
      return n && De.forEach(function($y) {
        return r(M, $y);
      }), vn && Ea(M, nt), He;
    }
    function An(M, D, z, se) {
      if (typeof z == "object" && z !== null && z.type === Ye && z.key === null && (z = z.props.children), typeof z == "object" && z !== null) {
        switch (z.$$typeof) {
          case ke:
            e: {
              for (var He = z.key, tt = D; tt !== null; ) {
                if (tt.key === He) {
                  if (He = z.type, He === Ye) {
                    if (tt.tag === 7) {
                      l(M, tt.sibling), D = c(tt, z.props.children), D.return = M, M = D;
                      break e;
                    }
                  } else if (tt.elementType === He || typeof He == "object" && He !== null && He.$$typeof === yt && Gv(He) === tt.type) {
                    l(M, tt.sibling), D = c(tt, z.props), D.ref = so(M, tt, z), D.return = M, M = D;
                    break e;
                  }
                  l(M, tt);
                  break;
                } else
                  r(M, tt);
                tt = tt.sibling;
              }
              z.type === Ye ? (D = Ro(z.props.children, M.mode, se, z.key), D.return = M, M = D) : (se = yf(z.type, z.key, z.props, null, M.mode, se), se.ref = so(M, D, z), se.return = M, M = se);
            }
            return m(M);
          case at:
            e: {
              for (tt = z.key; D !== null; ) {
                if (D.key === tt)
                  if (D.tag === 4 && D.stateNode.containerInfo === z.containerInfo && D.stateNode.implementation === z.implementation) {
                    l(M, D.sibling), D = c(D, z.children || []), D.return = M, M = D;
                    break e;
                  } else {
                    l(M, D);
                    break;
                  }
                else
                  r(M, D);
                D = D.sibling;
              }
              D = As(z, M.mode, se), D.return = M, M = D;
            }
            return m(M);
          case yt:
            return tt = z._init, An(M, D, tt(z._payload), se);
        }
        if (er(z))
          return _e(M, D, z, se);
        if (Ue(z))
          return Le(M, D, z, se);
        Ri(M, z);
      }
      return typeof z == "string" && z !== "" || typeof z == "number" ? (z = "" + z, D !== null && D.tag === 6 ? (l(M, D.sibling), D = c(D, z), D.return = M, M = D) : (l(M, D), D = Sf(z, M.mode, se), D.return = M, M = D), m(M)) : l(M, D);
    }
    return An;
  }
  var lu = Oc(!0), qv = Oc(!1), qi = xt(null), Qn = null, ve = null, $a = null;
  function Ra() {
    $a = ve = Qn = null;
  }
  function zd(n) {
    var r = qi.current;
    Gt(qi), n._currentValue = r;
  }
  function Ad(n, r, l) {
    for (; n !== null; ) {
      var u = n.alternate;
      if ((n.childLanes & r) !== r ? (n.childLanes |= r, u !== null && (u.childLanes |= r)) : u !== null && (u.childLanes & r) !== r && (u.childLanes |= r), n === l)
        break;
      n = n.return;
    }
  }
  function ou(n, r) {
    Qn = n, $a = ve = null, n = n.dependencies, n !== null && n.firstContext !== null && (n.lanes & r && (sa = !0), n.firstContext = null);
  }
  function Ia(n) {
    var r = n._currentValue;
    if ($a !== n)
      if (n = { context: n, memoizedValue: r, next: null }, ve === null) {
        if (Qn === null)
          throw Error(b(308));
        ve = n, Qn.dependencies = { lanes: 0, firstContext: n };
      } else
        ve = ve.next = n;
    return r;
  }
  var co = null;
  function Bn(n) {
    co === null ? co = [n] : co.push(n);
  }
  function Xv(n, r, l, u) {
    var c = r.interleaved;
    return c === null ? (l.next = l, Bn(r)) : (l.next = c.next, c.next = l), r.interleaved = l, Xi(n, u);
  }
  function Xi(n, r) {
    n.lanes |= r;
    var l = n.alternate;
    for (l !== null && (l.lanes |= r), l = n, n = n.return; n !== null; )
      n.childLanes |= r, l = n.alternate, l !== null && (l.childLanes |= r), l = n, n = n.return;
    return l.tag === 3 ? l.stateNode : null;
  }
  var Ml = !1;
  function Mc(n) {
    n.updateQueue = { baseState: n.memoizedState, firstBaseUpdate: null, lastBaseUpdate: null, shared: { pending: null, interleaved: null, lanes: 0 }, effects: null };
  }
  function uu(n, r) {
    n = n.updateQueue, r.updateQueue === n && (r.updateQueue = { baseState: n.baseState, firstBaseUpdate: n.firstBaseUpdate, lastBaseUpdate: n.lastBaseUpdate, shared: n.shared, effects: n.effects });
  }
  function oa(n, r) {
    return { eventTime: n, lane: r, tag: 0, payload: null, callback: null, next: null };
  }
  function Ll(n, r, l) {
    var u = n.updateQueue;
    if (u === null)
      return null;
    if (u = u.shared, Ot & 2) {
      var c = u.pending;
      return c === null ? r.next = r : (r.next = c.next, c.next = r), u.pending = r, Xi(n, l);
    }
    return c = u.interleaved, c === null ? (r.next = r, Bn(u)) : (r.next = c.next, c.next = r), u.interleaved = r, Xi(n, l);
  }
  function Lc(n, r, l) {
    if (r = r.updateQueue, r !== null && (r = r.shared, (l & 4194240) !== 0)) {
      var u = r.lanes;
      u &= n.pendingLanes, l |= u, r.lanes = l, bi(n, l);
    }
  }
  function Kv(n, r) {
    var l = n.updateQueue, u = n.alternate;
    if (u !== null && (u = u.updateQueue, l === u)) {
      var c = null, d = null;
      if (l = l.firstBaseUpdate, l !== null) {
        do {
          var m = { eventTime: l.eventTime, lane: l.lane, tag: l.tag, payload: l.payload, callback: l.callback, next: null };
          d === null ? c = d = m : d = d.next = m, l = l.next;
        } while (l !== null);
        d === null ? c = d = r : d = d.next = r;
      } else
        c = d = r;
      l = { baseState: u.baseState, firstBaseUpdate: c, lastBaseUpdate: d, shared: u.shared, effects: u.effects }, n.updateQueue = l;
      return;
    }
    n = l.lastBaseUpdate, n === null ? l.firstBaseUpdate = r : n.next = r, l.lastBaseUpdate = r;
  }
  function jc(n, r, l, u) {
    var c = n.updateQueue;
    Ml = !1;
    var d = c.firstBaseUpdate, m = c.lastBaseUpdate, E = c.shared.pending;
    if (E !== null) {
      c.shared.pending = null;
      var k = E, H = k.next;
      k.next = null, m === null ? d = H : m.next = H, m = k;
      var re = n.alternate;
      re !== null && (re = re.updateQueue, E = re.lastBaseUpdate, E !== m && (E === null ? re.firstBaseUpdate = H : E.next = H, re.lastBaseUpdate = k));
    }
    if (d !== null) {
      var ae = c.baseState;
      m = 0, re = H = k = null, E = d;
      do {
        var te = E.lane, Ce = E.eventTime;
        if ((u & te) === te) {
          re !== null && (re = re.next = {
            eventTime: Ce,
            lane: 0,
            tag: E.tag,
            payload: E.payload,
            callback: E.callback,
            next: null
          });
          e: {
            var _e = n, Le = E;
            switch (te = r, Ce = l, Le.tag) {
              case 1:
                if (_e = Le.payload, typeof _e == "function") {
                  ae = _e.call(Ce, ae, te);
                  break e;
                }
                ae = _e;
                break e;
              case 3:
                _e.flags = _e.flags & -65537 | 128;
              case 0:
                if (_e = Le.payload, te = typeof _e == "function" ? _e.call(Ce, ae, te) : _e, te == null)
                  break e;
                ae = pe({}, ae, te);
                break e;
              case 2:
                Ml = !0;
            }
          }
          E.callback !== null && E.lane !== 0 && (n.flags |= 64, te = c.effects, te === null ? c.effects = [E] : te.push(E));
        } else
          Ce = { eventTime: Ce, lane: te, tag: E.tag, payload: E.payload, callback: E.callback, next: null }, re === null ? (H = re = Ce, k = ae) : re = re.next = Ce, m |= te;
        if (E = E.next, E === null) {
          if (E = c.shared.pending, E === null)
            break;
          te = E, E = te.next, te.next = null, c.lastBaseUpdate = te, c.shared.pending = null;
        }
      } while (1);
      if (re === null && (k = ae), c.baseState = k, c.firstBaseUpdate = H, c.lastBaseUpdate = re, r = c.shared.interleaved, r !== null) {
        c = r;
        do
          m |= c.lane, c = c.next;
        while (c !== r);
      } else
        d === null && (c.shared.lanes = 0);
      bo |= m, n.lanes = m, n.memoizedState = ae;
    }
  }
  function Jv(n, r, l) {
    if (n = r.effects, r.effects = null, n !== null)
      for (r = 0; r < n.length; r++) {
        var u = n[r], c = u.callback;
        if (c !== null) {
          if (u.callback = null, u = l, typeof c != "function")
            throw Error(b(191, c));
          c.call(u);
        }
      }
  }
  var Ss = {}, di = xt(Ss), su = xt(Ss), xs = xt(Ss);
  function fo(n) {
    if (n === Ss)
      throw Error(b(174));
    return n;
  }
  function Ud(n, r) {
    switch (Zt(xs, r), Zt(su, n), Zt(di, Ss), n = r.nodeType, n) {
      case 9:
      case 11:
        r = (r = r.documentElement) ? r.namespaceURI : bn(null, "");
        break;
      default:
        n = n === 8 ? r.parentNode : r, r = n.namespaceURI || null, n = n.tagName, r = bn(r, n);
    }
    Gt(di), Zt(di, r);
  }
  function cu() {
    Gt(di), Gt(su), Gt(xs);
  }
  function Zv(n) {
    fo(xs.current);
    var r = fo(di.current), l = bn(r, n.type);
    r !== l && (Zt(su, n), Zt(di, l));
  }
  function Fd(n) {
    su.current === n && (Gt(di), Gt(su));
  }
  var gn = xt(0);
  function zc(n) {
    for (var r = n; r !== null; ) {
      if (r.tag === 13) {
        var l = r.memoizedState;
        if (l !== null && (l = l.dehydrated, l === null || l.data === "$?" || l.data === "$!"))
          return r;
      } else if (r.tag === 19 && r.memoizedProps.revealOrder !== void 0) {
        if (r.flags & 128)
          return r;
      } else if (r.child !== null) {
        r.child.return = r, r = r.child;
        continue;
      }
      if (r === n)
        break;
      for (; r.sibling === null; ) {
        if (r.return === null || r.return === n)
          return null;
        r = r.return;
      }
      r.sibling.return = r.return, r = r.sibling;
    }
    return null;
  }
  var Ac = [];
  function Hd() {
    for (var n = 0; n < Ac.length; n++)
      Ac[n]._workInProgressVersionPrimary = null;
    Ac.length = 0;
  }
  var Uc = ct.ReactCurrentDispatcher, bs = ct.ReactCurrentBatchConfig, Fe = 0, Ve = null, ut = null, _t = null, Ta = !1, fu = !1, Cs = 0, Ty = 0;
  function kr() {
    throw Error(b(321));
  }
  function Es(n, r) {
    if (r === null)
      return !1;
    for (var l = 0; l < r.length && l < n.length; l++)
      if (!Ua(n[l], r[l]))
        return !1;
    return !0;
  }
  function Z(n, r, l, u, c, d) {
    if (Fe = d, Ve = r, r.memoizedState = null, r.updateQueue = null, r.lanes = 0, Uc.current = n === null || n.memoizedState === null ? ky : fn, n = l(u, c), fu) {
      d = 0;
      do {
        if (fu = !1, Cs = 0, 25 <= d)
          throw Error(b(301));
        d += 1, _t = ut = null, r.updateQueue = null, Uc.current = Jc, n = l(u, c);
      } while (fu);
    }
    if (Uc.current = _r, r = ut !== null && ut.next !== null, Fe = 0, _t = ut = Ve = null, Ta = !1, r)
      throw Error(b(300));
    return n;
  }
  function $n() {
    var n = Cs !== 0;
    return Cs = 0, n;
  }
  function Qe() {
    var n = { memoizedState: null, baseState: null, baseQueue: null, queue: null, next: null };
    return _t === null ? Ve.memoizedState = _t = n : _t = _t.next = n, _t;
  }
  function fr() {
    if (ut === null) {
      var n = Ve.alternate;
      n = n !== null ? n.memoizedState : null;
    } else
      n = ut.next;
    var r = _t === null ? Ve.memoizedState : _t.next;
    if (r !== null)
      _t = r, ut = n;
    else {
      if (n === null)
        throw Error(b(310));
      ut = n, n = { memoizedState: ut.memoizedState, baseState: ut.baseState, baseQueue: ut.baseQueue, queue: ut.queue, next: null }, _t === null ? Ve.memoizedState = _t = n : _t = _t.next = n;
    }
    return _t;
  }
  function ka(n, r) {
    return typeof r == "function" ? r(n) : r;
  }
  function Ki(n) {
    var r = fr(), l = r.queue;
    if (l === null)
      throw Error(b(311));
    l.lastRenderedReducer = n;
    var u = ut, c = u.baseQueue, d = l.pending;
    if (d !== null) {
      if (c !== null) {
        var m = c.next;
        c.next = d.next, d.next = m;
      }
      u.baseQueue = c = d, l.pending = null;
    }
    if (c !== null) {
      d = c.next, u = u.baseState;
      var E = m = null, k = null, H = d;
      do {
        var re = H.lane;
        if ((Fe & re) === re)
          k !== null && (k = k.next = { lane: 0, action: H.action, hasEagerState: H.hasEagerState, eagerState: H.eagerState, next: null }), u = H.hasEagerState ? H.eagerState : n(u, H.action);
        else {
          var ae = {
            lane: re,
            action: H.action,
            hasEagerState: H.hasEagerState,
            eagerState: H.eagerState,
            next: null
          };
          k === null ? (E = k = ae, m = u) : k = k.next = ae, Ve.lanes |= re, bo |= re;
        }
        H = H.next;
      } while (H !== null && H !== d);
      k === null ? m = u : k.next = E, Ua(u, r.memoizedState) || (sa = !0), r.memoizedState = u, r.baseState = m, r.baseQueue = k, l.lastRenderedState = u;
    }
    if (n = l.interleaved, n !== null) {
      c = n;
      do
        d = c.lane, Ve.lanes |= d, bo |= d, c = c.next;
      while (c !== n);
    } else
      c === null && (l.lanes = 0);
    return [r.memoizedState, l.dispatch];
  }
  function Ya(n) {
    var r = fr(), l = r.queue;
    if (l === null)
      throw Error(b(311));
    l.lastRenderedReducer = n;
    var u = l.dispatch, c = l.pending, d = r.memoizedState;
    if (c !== null) {
      l.pending = null;
      var m = c = c.next;
      do
        d = n(d, m.action), m = m.next;
      while (m !== c);
      Ua(d, r.memoizedState) || (sa = !0), r.memoizedState = d, r.baseQueue === null && (r.baseState = d), l.lastRenderedState = d;
    }
    return [d, u];
  }
  function du() {
  }
  function po(n, r) {
    var l = Ve, u = fr(), c = r(), d = !Ua(u.memoizedState, c);
    if (d && (u.memoizedState = c, sa = !0), u = u.queue, ws(Hc.bind(null, l, u, n), [n]), u.getSnapshot !== r || d || _t !== null && _t.memoizedState.tag & 1) {
      if (l.flags |= 2048, vo(9, Fc.bind(null, l, u, c, r), void 0, null), Nn === null)
        throw Error(b(349));
      Fe & 30 || pu(l, r, c);
    }
    return c;
  }
  function pu(n, r, l) {
    n.flags |= 16384, n = { getSnapshot: r, value: l }, r = Ve.updateQueue, r === null ? (r = { lastEffect: null, stores: null }, Ve.updateQueue = r, r.stores = [n]) : (l = r.stores, l === null ? r.stores = [n] : l.push(n));
  }
  function Fc(n, r, l, u) {
    r.value = l, r.getSnapshot = u, Pc(r) && Vc(n);
  }
  function Hc(n, r, l) {
    return l(function() {
      Pc(r) && Vc(n);
    });
  }
  function Pc(n) {
    var r = n.getSnapshot;
    n = n.value;
    try {
      var l = r();
      return !Ua(n, l);
    } catch {
      return !0;
    }
  }
  function Vc(n) {
    var r = Xi(n, 1);
    r !== null && Rn(r, n, 1, -1);
  }
  function Bc(n) {
    var r = Qe();
    return typeof n == "function" && (n = n()), r.memoizedState = r.baseState = n, n = { pending: null, interleaved: null, lanes: 0, dispatch: null, lastRenderedReducer: ka, lastRenderedState: n }, r.queue = n, n = n.dispatch = Rs.bind(null, Ve, n), [r.memoizedState, n];
  }
  function vo(n, r, l, u) {
    return n = { tag: n, create: r, destroy: l, deps: u, next: null }, r = Ve.updateQueue, r === null ? (r = { lastEffect: null, stores: null }, Ve.updateQueue = r, r.lastEffect = n.next = n) : (l = r.lastEffect, l === null ? r.lastEffect = n.next = n : (u = l.next, l.next = n, n.next = u, r.lastEffect = n)), n;
  }
  function $c() {
    return fr().memoizedState;
  }
  function vu(n, r, l, u) {
    var c = Qe();
    Ve.flags |= n, c.memoizedState = vo(1 | r, l, void 0, u === void 0 ? null : u);
  }
  function hu(n, r, l, u) {
    var c = fr();
    u = u === void 0 ? null : u;
    var d = void 0;
    if (ut !== null) {
      var m = ut.memoizedState;
      if (d = m.destroy, u !== null && Es(u, m.deps)) {
        c.memoizedState = vo(r, l, d, u);
        return;
      }
    }
    Ve.flags |= n, c.memoizedState = vo(1 | r, l, d, u);
  }
  function Ic(n, r) {
    return vu(8390656, 8, n, r);
  }
  function ws(n, r) {
    return hu(2048, 8, n, r);
  }
  function Yc(n, r) {
    return hu(4, 2, n, r);
  }
  function Wc(n, r) {
    return hu(4, 4, n, r);
  }
  function Qc(n, r) {
    if (typeof r == "function")
      return n = n(), r(n), function() {
        r(null);
      };
    if (r != null)
      return n = n(), r.current = n, function() {
        r.current = null;
      };
  }
  function Gc(n, r, l) {
    return l = l != null ? l.concat([n]) : null, hu(4, 4, Qc.bind(null, r, n), l);
  }
  function mu() {
  }
  function ho(n, r) {
    var l = fr();
    r = r === void 0 ? null : r;
    var u = l.memoizedState;
    return u !== null && r !== null && Es(r, u[1]) ? u[0] : (l.memoizedState = [n, r], n);
  }
  function qc(n, r) {
    var l = fr();
    r = r === void 0 ? null : r;
    var u = l.memoizedState;
    return u !== null && r !== null && Es(r, u[1]) ? u[0] : (n = n(), l.memoizedState = [n, r], n);
  }
  function Xc(n, r, l) {
    return Fe & 21 ? (Ua(l, r) || (l = $o(), Ve.lanes |= l, bo |= l, n.baseState = !0), r) : (n.baseState && (n.baseState = !1, sa = !0), n.memoizedState = l);
  }
  function Pd(n, r) {
    var l = Bt;
    Bt = l !== 0 && 4 > l ? l : 4, n(!0);
    var u = bs.transition;
    bs.transition = {};
    try {
      n(!1), r();
    } finally {
      Bt = l, bs.transition = u;
    }
  }
  function Kc() {
    return fr().memoizedState;
  }
  function eh(n, r, l) {
    var u = el(n);
    if (l = { lane: u, action: l, hasEagerState: !1, eagerState: null, next: null }, Vd(n))
      yu(r, l);
    else if (l = Xv(n, r, l, u), l !== null) {
      var c = or();
      Rn(l, n, u, c), jl(l, r, u);
    }
  }
  function Rs(n, r, l) {
    var u = el(n), c = { lane: u, action: l, hasEagerState: !1, eagerState: null, next: null };
    if (Vd(n))
      yu(r, c);
    else {
      var d = n.alternate;
      if (n.lanes === 0 && (d === null || d.lanes === 0) && (d = r.lastRenderedReducer, d !== null))
        try {
          var m = r.lastRenderedState, E = d(m, l);
          if (c.hasEagerState = !0, c.eagerState = E, Ua(E, m)) {
            var k = r.interleaved;
            k === null ? (c.next = c, Bn(r)) : (c.next = k.next, k.next = c), r.interleaved = c;
            return;
          }
        } catch {
        } finally {
        }
      l = Xv(n, r, c, u), l !== null && (c = or(), Rn(l, n, u, c), jl(l, r, u));
    }
  }
  function Vd(n) {
    var r = n.alternate;
    return n === Ve || r !== null && r === Ve;
  }
  function yu(n, r) {
    fu = Ta = !0;
    var l = n.pending;
    l === null ? r.next = r : (r.next = l.next, l.next = r), n.pending = r;
  }
  function jl(n, r, l) {
    if (l & 4194240) {
      var u = r.lanes;
      u &= n.pendingLanes, l |= u, r.lanes = l, bi(n, l);
    }
  }
  var _r = { readContext: Ia, useCallback: kr, useContext: kr, useEffect: kr, useImperativeHandle: kr, useInsertionEffect: kr, useLayoutEffect: kr, useMemo: kr, useReducer: kr, useRef: kr, useState: kr, useDebugValue: kr, useDeferredValue: kr, useTransition: kr, useMutableSource: kr, useSyncExternalStore: kr, useId: kr, unstable_isNewReconciler: !1 }, ky = { readContext: Ia, useCallback: function(n, r) {
    return Qe().memoizedState = [n, r === void 0 ? null : r], n;
  }, useContext: Ia, useEffect: Ic, useImperativeHandle: function(n, r, l) {
    return l = l != null ? l.concat([n]) : null, vu(
      4194308,
      4,
      Qc.bind(null, r, n),
      l
    );
  }, useLayoutEffect: function(n, r) {
    return vu(4194308, 4, n, r);
  }, useInsertionEffect: function(n, r) {
    return vu(4, 2, n, r);
  }, useMemo: function(n, r) {
    var l = Qe();
    return r = r === void 0 ? null : r, n = n(), l.memoizedState = [n, r], n;
  }, useReducer: function(n, r, l) {
    var u = Qe();
    return r = l !== void 0 ? l(r) : r, u.memoizedState = u.baseState = r, n = { pending: null, interleaved: null, lanes: 0, dispatch: null, lastRenderedReducer: n, lastRenderedState: r }, u.queue = n, n = n.dispatch = eh.bind(null, Ve, n), [u.memoizedState, n];
  }, useRef: function(n) {
    var r = Qe();
    return n = { current: n }, r.memoizedState = n;
  }, useState: Bc, useDebugValue: mu, useDeferredValue: function(n) {
    return Qe().memoizedState = n;
  }, useTransition: function() {
    var n = Bc(!1), r = n[0];
    return n = Pd.bind(null, n[1]), Qe().memoizedState = n, [r, n];
  }, useMutableSource: function() {
  }, useSyncExternalStore: function(n, r, l) {
    var u = Ve, c = Qe();
    if (vn) {
      if (l === void 0)
        throw Error(b(407));
      l = l();
    } else {
      if (l = r(), Nn === null)
        throw Error(b(349));
      Fe & 30 || pu(u, r, l);
    }
    c.memoizedState = l;
    var d = { value: l, getSnapshot: r };
    return c.queue = d, Ic(Hc.bind(
      null,
      u,
      d,
      n
    ), [n]), u.flags |= 2048, vo(9, Fc.bind(null, u, d, l, r), void 0, null), l;
  }, useId: function() {
    var n = Qe(), r = Nn.identifierPrefix;
    if (vn) {
      var l = Gi, u = cr;
      l = (u & ~(1 << 32 - zr(u) - 1)).toString(32) + l, r = ":" + r + "R" + l, l = Cs++, 0 < l && (r += "H" + l.toString(32)), r += ":";
    } else
      l = Ty++, r = ":" + r + "r" + l.toString(32) + ":";
    return n.memoizedState = r;
  }, unstable_isNewReconciler: !1 }, fn = {
    readContext: Ia,
    useCallback: ho,
    useContext: Ia,
    useEffect: ws,
    useImperativeHandle: Gc,
    useInsertionEffect: Yc,
    useLayoutEffect: Wc,
    useMemo: qc,
    useReducer: Ki,
    useRef: $c,
    useState: function() {
      return Ki(ka);
    },
    useDebugValue: mu,
    useDeferredValue: function(n) {
      var r = fr();
      return Xc(r, ut.memoizedState, n);
    },
    useTransition: function() {
      var n = Ki(ka)[0], r = fr().memoizedState;
      return [n, r];
    },
    useMutableSource: du,
    useSyncExternalStore: po,
    useId: Kc,
    unstable_isNewReconciler: !1
  }, Jc = { readContext: Ia, useCallback: ho, useContext: Ia, useEffect: ws, useImperativeHandle: Gc, useInsertionEffect: Yc, useLayoutEffect: Wc, useMemo: qc, useReducer: Ya, useRef: $c, useState: function() {
    return Ya(ka);
  }, useDebugValue: mu, useDeferredValue: function(n) {
    var r = fr();
    return ut === null ? r.memoizedState = n : Xc(r, ut.memoizedState, n);
  }, useTransition: function() {
    var n = Ya(ka)[0], r = fr().memoizedState;
    return [n, r];
  }, useMutableSource: du, useSyncExternalStore: po, useId: Kc, unstable_isNewReconciler: !1 };
  function ua(n, r) {
    if (n && n.defaultProps) {
      r = pe({}, r), n = n.defaultProps;
      for (var l in n)
        r[l] === void 0 && (r[l] = n[l]);
      return r;
    }
    return r;
  }
  function mo(n, r, l, u) {
    r = n.memoizedState, l = l(u, r), l = l == null ? r : pe({}, r, l), n.memoizedState = l, n.lanes === 0 && (n.updateQueue.baseState = l);
  }
  var yo = { isMounted: function(n) {
    return (n = n._reactInternals) ? Pe(n) === n : !1;
  }, enqueueSetState: function(n, r, l) {
    n = n._reactInternals;
    var u = or(), c = el(n), d = oa(u, c);
    d.payload = r, l != null && (d.callback = l), r = Ll(n, d, c), r !== null && (Rn(r, n, c, u), Lc(r, n, c));
  }, enqueueReplaceState: function(n, r, l) {
    n = n._reactInternals;
    var u = or(), c = el(n), d = oa(u, c);
    d.tag = 1, d.payload = r, l != null && (d.callback = l), r = Ll(n, d, c), r !== null && (Rn(r, n, c, u), Lc(r, n, c));
  }, enqueueForceUpdate: function(n, r) {
    n = n._reactInternals;
    var l = or(), u = el(n), c = oa(l, u);
    c.tag = 2, r != null && (c.callback = r), r = Ll(n, c, u), r !== null && (Rn(r, n, u, l), Lc(r, n, u));
  } };
  function th(n, r, l, u, c, d, m) {
    return n = n.stateNode, typeof n.shouldComponentUpdate == "function" ? n.shouldComponentUpdate(u, d, m) : r.prototype && r.prototype.isPureReactComponent ? !os(l, u) || !os(c, d) : !0;
  }
  function nh(n, r, l) {
    var u = !1, c = wi, d = r.contextType;
    return typeof d == "object" && d !== null ? d = Ia(d) : (c = yn(r) ? na : ot.current, u = r.contextTypes, d = (u = u != null) ? Ha(n, c) : wi), r = new r(l, d), n.memoizedState = r.state !== null && r.state !== void 0 ? r.state : null, r.updater = yo, n.stateNode = r, r._reactInternals = n, u && (n = n.stateNode, n.__reactInternalMemoizedUnmaskedChildContext = c, n.__reactInternalMemoizedMaskedChildContext = d), r;
  }
  function rh(n, r, l, u) {
    n = r.state, typeof r.componentWillReceiveProps == "function" && r.componentWillReceiveProps(l, u), typeof r.UNSAFE_componentWillReceiveProps == "function" && r.UNSAFE_componentWillReceiveProps(l, u), r.state !== n && yo.enqueueReplaceState(r, r.state, null);
  }
  function Bd(n, r, l, u) {
    var c = n.stateNode;
    c.props = l, c.state = n.memoizedState, c.refs = {}, Mc(n);
    var d = r.contextType;
    typeof d == "object" && d !== null ? c.context = Ia(d) : (d = yn(r) ? na : ot.current, c.context = Ha(n, d)), c.state = n.memoizedState, d = r.getDerivedStateFromProps, typeof d == "function" && (mo(n, r, d, l), c.state = n.memoizedState), typeof r.getDerivedStateFromProps == "function" || typeof c.getSnapshotBeforeUpdate == "function" || typeof c.UNSAFE_componentWillMount != "function" && typeof c.componentWillMount != "function" || (r = c.state, typeof c.componentWillMount == "function" && c.componentWillMount(), typeof c.UNSAFE_componentWillMount == "function" && c.UNSAFE_componentWillMount(), r !== c.state && yo.enqueueReplaceState(c, c.state, null), jc(n, l, c, u), c.state = n.memoizedState), typeof c.componentDidMount == "function" && (n.flags |= 4194308);
  }
  function zl(n, r) {
    try {
      var l = "", u = r;
      do
        l += ft(u), u = u.return;
      while (u);
      var c = l;
    } catch (d) {
      c = `
Error generating stack: ` + d.message + `
` + d.stack;
    }
    return { value: n, source: r, stack: c, digest: null };
  }
  function $d(n, r, l) {
    return { value: n, source: null, stack: l ?? null, digest: r ?? null };
  }
  function Ts(n, r) {
    try {
      console.error(r.value);
    } catch (l) {
      setTimeout(function() {
        throw l;
      });
    }
  }
  var ah = typeof WeakMap == "function" ? WeakMap : Map;
  function ih(n, r, l) {
    l = oa(-1, l), l.tag = 3, l.payload = { element: null };
    var u = r.value;
    return l.callback = function() {
      ff || (ff = !0, Jd = u), Ts(n, r);
    }, l;
  }
  function lh(n, r, l) {
    l = oa(-1, l), l.tag = 3;
    var u = n.type.getDerivedStateFromError;
    if (typeof u == "function") {
      var c = r.value;
      l.payload = function() {
        return u(c);
      }, l.callback = function() {
        Ts(n, r);
      };
    }
    var d = n.stateNode;
    return d !== null && typeof d.componentDidCatch == "function" && (l.callback = function() {
      Ts(n, r), typeof u != "function" && (Ga === null ? Ga = /* @__PURE__ */ new Set([this]) : Ga.add(this));
      var m = r.stack;
      this.componentDidCatch(r.value, { componentStack: m !== null ? m : "" });
    }), l;
  }
  function ks(n, r, l) {
    var u = n.pingCache;
    if (u === null) {
      u = n.pingCache = new ah();
      var c = /* @__PURE__ */ new Set();
      u.set(r, c);
    } else
      c = u.get(r), c === void 0 && (c = /* @__PURE__ */ new Set(), u.set(r, c));
    c.has(l) || (c.add(l), n = Uy.bind(null, n, r, l), r.then(n, n));
  }
  function oh(n) {
    do {
      var r;
      if ((r = n.tag === 13) && (r = n.memoizedState, r = r !== null ? r.dehydrated !== null : !0), r)
        return n;
      n = n.return;
    } while (n !== null);
    return null;
  }
  function Id(n, r, l, u, c) {
    return n.mode & 1 ? (n.flags |= 65536, n.lanes = c, n) : (n === r ? n.flags |= 65536 : (n.flags |= 128, l.flags |= 131072, l.flags &= -52805, l.tag === 1 && (l.alternate === null ? l.tag = 17 : (r = oa(-1, 1), r.tag = 2, Ll(l, r, 1))), l.lanes |= 1), n);
  }
  var uh = ct.ReactCurrentOwner, sa = !1;
  function jn(n, r, l, u) {
    r.child = n === null ? qv(r, null, l, u) : lu(r, n.child, l, u);
  }
  function gu(n, r, l, u, c) {
    l = l.render;
    var d = r.ref;
    return ou(r, c), u = Z(n, r, l, u, d, c), l = $n(), n !== null && !sa ? (r.updateQueue = n.updateQueue, r.flags &= -2053, n.lanes &= ~c, zn(n, r, c)) : (vn && l && Tc(r), r.flags |= 1, jn(n, r, u, c), r.child);
  }
  function Al(n, r, l, u, c) {
    if (n === null) {
      var d = l.type;
      return typeof d == "function" && !rp(d) && d.defaultProps === void 0 && l.compare === null && l.defaultProps === void 0 ? (r.tag = 15, r.type = d, Zc(n, r, d, u, c)) : (n = yf(l.type, null, u, r, r.mode, c), n.ref = r.ref, n.return = r, r.child = n);
    }
    if (d = n.child, !(n.lanes & c)) {
      var m = d.memoizedProps;
      if (l = l.compare, l = l !== null ? l : os, l(m, u) && n.ref === r.ref)
        return zn(n, r, c);
    }
    return r.flags |= 1, n = Hl(d, u), n.ref = r.ref, n.return = r, r.child = n;
  }
  function Zc(n, r, l, u, c) {
    if (n !== null) {
      var d = n.memoizedProps;
      if (os(d, u) && n.ref === r.ref)
        if (sa = !1, r.pendingProps = u = d, (n.lanes & c) !== 0)
          n.flags & 131072 && (sa = !0);
        else
          return r.lanes = n.lanes, zn(n, r, c);
    }
    return gt(n, r, l, u, c);
  }
  function ca(n, r, l) {
    var u = r.pendingProps, c = u.children, d = n !== null ? n.memoizedState : null;
    if (u.mode === "hidden")
      if (!(r.mode & 1))
        r.memoizedState = { baseLanes: 0, cachePool: null, transitions: null }, Zt(_u, fa), fa |= l;
      else {
        if (!(l & 1073741824))
          return n = d !== null ? d.baseLanes | l : l, r.lanes = r.childLanes = 1073741824, r.memoizedState = { baseLanes: n, cachePool: null, transitions: null }, r.updateQueue = null, Zt(_u, fa), fa |= n, null;
        r.memoizedState = { baseLanes: 0, cachePool: null, transitions: null }, u = d !== null ? d.baseLanes : l, Zt(_u, fa), fa |= u;
      }
    else
      d !== null ? (u = d.baseLanes | l, r.memoizedState = null) : u = l, Zt(_u, fa), fa |= u;
    return jn(n, r, c, l), r.child;
  }
  function go(n, r) {
    var l = r.ref;
    (n === null && l !== null || n !== null && n.ref !== l) && (r.flags |= 512, r.flags |= 2097152);
  }
  function gt(n, r, l, u, c) {
    var d = yn(l) ? na : ot.current;
    return d = Ha(r, d), ou(r, c), l = Z(n, r, l, u, d, c), u = $n(), n !== null && !sa ? (r.updateQueue = n.updateQueue, r.flags &= -2053, n.lanes &= ~c, zn(n, r, c)) : (vn && u && Tc(r), r.flags |= 1, jn(n, r, l, c), r.child);
  }
  function _s(n, r, l, u, c) {
    if (yn(l)) {
      var d = !0;
      Rc(r);
    } else
      d = !1;
    if (ou(r, c), r.stateNode === null)
      Ns(n, r), nh(r, l, u), Bd(r, l, u, c), u = !0;
    else if (n === null) {
      var m = r.stateNode, E = r.memoizedProps;
      m.props = E;
      var k = m.context, H = l.contextType;
      typeof H == "object" && H !== null ? H = Ia(H) : (H = yn(l) ? na : ot.current, H = Ha(r, H));
      var re = l.getDerivedStateFromProps, ae = typeof re == "function" || typeof m.getSnapshotBeforeUpdate == "function";
      ae || typeof m.UNSAFE_componentWillReceiveProps != "function" && typeof m.componentWillReceiveProps != "function" || (E !== u || k !== H) && rh(r, m, u, H), Ml = !1;
      var te = r.memoizedState;
      m.state = te, jc(r, u, m, c), k = r.memoizedState, E !== u || te !== k || _n.current || Ml ? (typeof re == "function" && (mo(r, l, re, u), k = r.memoizedState), (E = Ml || th(r, l, E, u, te, k, H)) ? (ae || typeof m.UNSAFE_componentWillMount != "function" && typeof m.componentWillMount != "function" || (typeof m.componentWillMount == "function" && m.componentWillMount(), typeof m.UNSAFE_componentWillMount == "function" && m.UNSAFE_componentWillMount()), typeof m.componentDidMount == "function" && (r.flags |= 4194308)) : (typeof m.componentDidMount == "function" && (r.flags |= 4194308), r.memoizedProps = u, r.memoizedState = k), m.props = u, m.state = k, m.context = H, u = E) : (typeof m.componentDidMount == "function" && (r.flags |= 4194308), u = !1);
    } else {
      m = r.stateNode, uu(n, r), E = r.memoizedProps, H = r.type === r.elementType ? E : ua(r.type, E), m.props = H, ae = r.pendingProps, te = m.context, k = l.contextType, typeof k == "object" && k !== null ? k = Ia(k) : (k = yn(l) ? na : ot.current, k = Ha(r, k));
      var Ce = l.getDerivedStateFromProps;
      (re = typeof Ce == "function" || typeof m.getSnapshotBeforeUpdate == "function") || typeof m.UNSAFE_componentWillReceiveProps != "function" && typeof m.componentWillReceiveProps != "function" || (E !== ae || te !== k) && rh(r, m, u, k), Ml = !1, te = r.memoizedState, m.state = te, jc(r, u, m, c);
      var _e = r.memoizedState;
      E !== ae || te !== _e || _n.current || Ml ? (typeof Ce == "function" && (mo(r, l, Ce, u), _e = r.memoizedState), (H = Ml || th(r, l, H, u, te, _e, k) || !1) ? (re || typeof m.UNSAFE_componentWillUpdate != "function" && typeof m.componentWillUpdate != "function" || (typeof m.componentWillUpdate == "function" && m.componentWillUpdate(u, _e, k), typeof m.UNSAFE_componentWillUpdate == "function" && m.UNSAFE_componentWillUpdate(u, _e, k)), typeof m.componentDidUpdate == "function" && (r.flags |= 4), typeof m.getSnapshotBeforeUpdate == "function" && (r.flags |= 1024)) : (typeof m.componentDidUpdate != "function" || E === n.memoizedProps && te === n.memoizedState || (r.flags |= 4), typeof m.getSnapshotBeforeUpdate != "function" || E === n.memoizedProps && te === n.memoizedState || (r.flags |= 1024), r.memoizedProps = u, r.memoizedState = _e), m.props = u, m.state = _e, m.context = k, u = H) : (typeof m.componentDidUpdate != "function" || E === n.memoizedProps && te === n.memoizedState || (r.flags |= 4), typeof m.getSnapshotBeforeUpdate != "function" || E === n.memoizedProps && te === n.memoizedState || (r.flags |= 1024), u = !1);
    }
    return ef(n, r, l, u, d, c);
  }
  function ef(n, r, l, u, c, d) {
    go(n, r);
    var m = (r.flags & 128) !== 0;
    if (!u && !m)
      return c && Iv(r, l, !1), zn(n, r, d);
    u = r.stateNode, uh.current = r;
    var E = m && typeof l.getDerivedStateFromError != "function" ? null : u.render();
    return r.flags |= 1, n !== null && m ? (r.child = lu(r, n.child, null, d), r.child = lu(r, null, E, d)) : jn(n, r, E, d), r.memoizedState = u.state, c && Iv(r, l, !0), r.child;
  }
  function _y(n) {
    var r = n.stateNode;
    r.pendingContext ? Nl(n, r.pendingContext, r.pendingContext !== r.context) : r.context && Nl(n, r.context, !1), Ud(n, r.containerInfo);
  }
  function sh(n, r, l, u, c) {
    return wn(), jd(c), r.flags |= 256, jn(n, r, l, u), r.child;
  }
  var Ds = { dehydrated: null, treeContext: null, retryLane: 0 };
  function So(n) {
    return { baseLanes: n, cachePool: null, transitions: null };
  }
  function ch(n, r, l) {
    var u = r.pendingProps, c = gn.current, d = !1, m = (r.flags & 128) !== 0, E;
    if ((E = m) || (E = n !== null && n.memoizedState === null ? !1 : (c & 2) !== 0), E ? (d = !0, r.flags &= -129) : (n === null || n.memoizedState !== null) && (c |= 1), Zt(gn, c & 1), n === null)
      return _c(r), n = r.memoizedState, n !== null && (n = n.dehydrated, n !== null) ? (r.mode & 1 ? n.data === "$!" ? r.lanes = 8 : r.lanes = 1073741824 : r.lanes = 1, null) : (m = u.children, n = u.fallback, d ? (u = r.mode, d = r.child, m = { mode: "hidden", children: m }, !(u & 1) && d !== null ? (d.childLanes = 0, d.pendingProps = m) : d = gf(m, u, 0, null), n = Ro(n, u, l, null), d.return = r, n.return = r, d.sibling = n, r.child = d, r.child.memoizedState = So(l), r.memoizedState = Ds, n) : tf(r, m));
    if (c = n.memoizedState, c !== null && (E = c.dehydrated, E !== null))
      return Yd(n, r, m, u, E, c, l);
    if (d) {
      d = u.fallback, m = r.mode, c = n.child, E = c.sibling;
      var k = { mode: "hidden", children: u.children };
      return !(m & 1) && r.child !== c ? (u = r.child, u.childLanes = 0, u.pendingProps = k, r.deletions = null) : (u = Hl(c, k), u.subtreeFlags = c.subtreeFlags & 14680064), E !== null ? d = Hl(E, d) : (d = Ro(d, m, l, null), d.flags |= 2), d.return = r, u.return = r, u.sibling = d, r.child = u, u = d, d = r.child, m = n.child.memoizedState, m = m === null ? So(l) : { baseLanes: m.baseLanes | l, cachePool: null, transitions: m.transitions }, d.memoizedState = m, d.childLanes = n.childLanes & ~l, r.memoizedState = Ds, u;
    }
    return d = n.child, n = d.sibling, u = Hl(d, { mode: "visible", children: u.children }), !(r.mode & 1) && (u.lanes = l), u.return = r, u.sibling = null, n !== null && (l = r.deletions, l === null ? (r.deletions = [n], r.flags |= 16) : l.push(n)), r.child = u, r.memoizedState = null, u;
  }
  function tf(n, r) {
    return r = gf({ mode: "visible", children: r }, n.mode, 0, null), r.return = n, n.child = r;
  }
  function nf(n, r, l, u) {
    return u !== null && jd(u), lu(r, n.child, null, l), n = tf(r, r.pendingProps.children), n.flags |= 2, r.memoizedState = null, n;
  }
  function Yd(n, r, l, u, c, d, m) {
    if (l)
      return r.flags & 256 ? (r.flags &= -257, u = $d(Error(b(422))), nf(n, r, m, u)) : r.memoizedState !== null ? (r.child = n.child, r.flags |= 128, null) : (d = u.fallback, c = r.mode, u = gf({ mode: "visible", children: u.children }, c, 0, null), d = Ro(d, c, m, null), d.flags |= 2, u.return = r, d.return = r, u.sibling = d, r.child = u, r.mode & 1 && lu(r, n.child, null, m), r.child.memoizedState = So(m), r.memoizedState = Ds, d);
    if (!(r.mode & 1))
      return nf(n, r, m, null);
    if (c.data === "$!") {
      if (u = c.nextSibling && c.nextSibling.dataset, u)
        var E = u.dgst;
      return u = E, d = Error(b(419)), u = $d(d, u, void 0), nf(n, r, m, u);
    }
    if (E = (m & n.childLanes) !== 0, sa || E) {
      if (u = Nn, u !== null) {
        switch (m & -m) {
          case 4:
            c = 2;
            break;
          case 16:
            c = 8;
            break;
          case 64:
          case 128:
          case 256:
          case 512:
          case 1024:
          case 2048:
          case 4096:
          case 8192:
          case 16384:
          case 32768:
          case 65536:
          case 131072:
          case 262144:
          case 524288:
          case 1048576:
          case 2097152:
          case 4194304:
          case 8388608:
          case 16777216:
          case 33554432:
          case 67108864:
            c = 32;
            break;
          case 536870912:
            c = 268435456;
            break;
          default:
            c = 0;
        }
        c = c & (u.suspendedLanes | m) ? 0 : c, c !== 0 && c !== d.retryLane && (d.retryLane = c, Xi(n, c), Rn(u, n, c, -1));
      }
      return zs(), u = $d(Error(b(421))), nf(n, r, m, u);
    }
    return c.data === "$?" ? (r.flags |= 128, r.child = n.child, r = np.bind(null, n), c._reactRetry = r, null) : (n = d.treeContext, la = fi(c.nextSibling), wa = r, vn = !0, Ba = null, n !== null && (ia[Tr++] = cr, ia[Tr++] = Gi, ia[Tr++] = Va, cr = n.id, Gi = n.overflow, Va = r), r = tf(r, u.children), r.flags |= 4096, r);
  }
  function fh(n, r, l) {
    n.lanes |= r;
    var u = n.alternate;
    u !== null && (u.lanes |= r), Ad(n.return, r, l);
  }
  function rf(n, r, l, u, c) {
    var d = n.memoizedState;
    d === null ? n.memoizedState = { isBackwards: r, rendering: null, renderingStartTime: 0, last: u, tail: l, tailMode: c } : (d.isBackwards = r, d.rendering = null, d.renderingStartTime = 0, d.last = u, d.tail = l, d.tailMode = c);
  }
  function Wd(n, r, l) {
    var u = r.pendingProps, c = u.revealOrder, d = u.tail;
    if (jn(n, r, u.children, l), u = gn.current, u & 2)
      u = u & 1 | 2, r.flags |= 128;
    else {
      if (n !== null && n.flags & 128)
        e:
          for (n = r.child; n !== null; ) {
            if (n.tag === 13)
              n.memoizedState !== null && fh(n, l, r);
            else if (n.tag === 19)
              fh(n, l, r);
            else if (n.child !== null) {
              n.child.return = n, n = n.child;
              continue;
            }
            if (n === r)
              break e;
            for (; n.sibling === null; ) {
              if (n.return === null || n.return === r)
                break e;
              n = n.return;
            }
            n.sibling.return = n.return, n = n.sibling;
          }
      u &= 1;
    }
    if (Zt(gn, u), !(r.mode & 1))
      r.memoizedState = null;
    else
      switch (c) {
        case "forwards":
          for (l = r.child, c = null; l !== null; )
            n = l.alternate, n !== null && zc(n) === null && (c = l), l = l.sibling;
          l = c, l === null ? (c = r.child, r.child = null) : (c = l.sibling, l.sibling = null), rf(r, !1, c, l, d);
          break;
        case "backwards":
          for (l = null, c = r.child, r.child = null; c !== null; ) {
            if (n = c.alternate, n !== null && zc(n) === null) {
              r.child = c;
              break;
            }
            n = c.sibling, c.sibling = l, l = c, c = n;
          }
          rf(r, !0, l, null, d);
          break;
        case "together":
          rf(r, !1, null, null, void 0);
          break;
        default:
          r.memoizedState = null;
      }
    return r.child;
  }
  function Ns(n, r) {
    !(r.mode & 1) && n !== null && (n.alternate = null, r.alternate = null, r.flags |= 2);
  }
  function zn(n, r, l) {
    if (n !== null && (r.dependencies = n.dependencies), bo |= r.lanes, !(l & r.childLanes))
      return null;
    if (n !== null && r.child !== n.child)
      throw Error(b(153));
    if (r.child !== null) {
      for (n = r.child, l = Hl(n, n.pendingProps), r.child = l, l.return = r; n.sibling !== null; )
        n = n.sibling, l = l.sibling = Hl(n, n.pendingProps), l.return = r;
      l.sibling = null;
    }
    return r.child;
  }
  function Ji(n, r, l) {
    switch (r.tag) {
      case 3:
        _y(r), wn();
        break;
      case 5:
        Zv(r);
        break;
      case 1:
        yn(r.type) && Rc(r);
        break;
      case 4:
        Ud(r, r.stateNode.containerInfo);
        break;
      case 10:
        var u = r.type._context, c = r.memoizedProps.value;
        Zt(qi, u._currentValue), u._currentValue = c;
        break;
      case 13:
        if (u = r.memoizedState, u !== null)
          return u.dehydrated !== null ? (Zt(gn, gn.current & 1), r.flags |= 128, null) : l & r.child.childLanes ? ch(n, r, l) : (Zt(gn, gn.current & 1), n = zn(n, r, l), n !== null ? n.sibling : null);
        Zt(gn, gn.current & 1);
        break;
      case 19:
        if (u = (l & r.childLanes) !== 0, n.flags & 128) {
          if (u)
            return Wd(n, r, l);
          r.flags |= 128;
        }
        if (c = r.memoizedState, c !== null && (c.rendering = null, c.tail = null, c.lastEffect = null), Zt(gn, gn.current), u)
          break;
        return null;
      case 22:
      case 23:
        return r.lanes = 0, ca(n, r, l);
    }
    return zn(n, r, l);
  }
  var Ti, Su, xu, Wa;
  Ti = function(n, r) {
    for (var l = r.child; l !== null; ) {
      if (l.tag === 5 || l.tag === 6)
        n.appendChild(l.stateNode);
      else if (l.tag !== 4 && l.child !== null) {
        l.child.return = l, l = l.child;
        continue;
      }
      if (l === r)
        break;
      for (; l.sibling === null; ) {
        if (l.return === null || l.return === r)
          return;
        l = l.return;
      }
      l.sibling.return = l.return, l = l.sibling;
    }
  }, Su = function() {
  }, xu = function(n, r, l, u) {
    var c = n.memoizedProps;
    if (c !== u) {
      n = r.stateNode, fo(di.current);
      var d = null;
      switch (l) {
        case "input":
          c = Zn(n, c), u = Zn(n, u), d = [];
          break;
        case "select":
          c = pe({}, c, { value: void 0 }), u = pe({}, u, { value: void 0 }), d = [];
          break;
        case "textarea":
          c = Xr(n, c), u = Xr(n, u), d = [];
          break;
        default:
          typeof c.onClick != "function" && typeof u.onClick == "function" && (n.onclick = wc);
      }
      Ln(l, u);
      var m;
      l = null;
      for (H in c)
        if (!u.hasOwnProperty(H) && c.hasOwnProperty(H) && c[H] != null)
          if (H === "style") {
            var E = c[H];
            for (m in E)
              E.hasOwnProperty(m) && (l || (l = {}), l[m] = "");
          } else
            H !== "dangerouslySetInnerHTML" && H !== "children" && H !== "suppressContentEditableWarning" && H !== "suppressHydrationWarning" && H !== "autoFocus" && (X.hasOwnProperty(H) ? d || (d = []) : (d = d || []).push(H, null));
      for (H in u) {
        var k = u[H];
        if (E = c != null ? c[H] : void 0, u.hasOwnProperty(H) && k !== E && (k != null || E != null))
          if (H === "style")
            if (E) {
              for (m in E)
                !E.hasOwnProperty(m) || k && k.hasOwnProperty(m) || (l || (l = {}), l[m] = "");
              for (m in k)
                k.hasOwnProperty(m) && E[m] !== k[m] && (l || (l = {}), l[m] = k[m]);
            } else
              l || (d || (d = []), d.push(
                H,
                l
              )), l = k;
          else
            H === "dangerouslySetInnerHTML" ? (k = k ? k.__html : void 0, E = E ? E.__html : void 0, k != null && E !== k && (d = d || []).push(H, k)) : H === "children" ? typeof k != "string" && typeof k != "number" || (d = d || []).push(H, "" + k) : H !== "suppressContentEditableWarning" && H !== "suppressHydrationWarning" && (X.hasOwnProperty(H) ? (k != null && H === "onScroll" && sn("scroll", n), d || E === k || (d = [])) : (d = d || []).push(H, k));
      }
      l && (d = d || []).push("style", l);
      var H = d;
      (r.updateQueue = H) && (r.flags |= 4);
    }
  }, Wa = function(n, r, l, u) {
    l !== u && (r.flags |= 4);
  };
  function Dn(n, r) {
    if (!vn)
      switch (n.tailMode) {
        case "hidden":
          r = n.tail;
          for (var l = null; r !== null; )
            r.alternate !== null && (l = r), r = r.sibling;
          l === null ? n.tail = null : l.sibling = null;
          break;
        case "collapsed":
          l = n.tail;
          for (var u = null; l !== null; )
            l.alternate !== null && (u = l), l = l.sibling;
          u === null ? r || n.tail === null ? n.tail = null : n.tail.sibling = null : u.sibling = null;
      }
  }
  function Dr(n) {
    var r = n.alternate !== null && n.alternate.child === n.child, l = 0, u = 0;
    if (r)
      for (var c = n.child; c !== null; )
        l |= c.lanes | c.childLanes, u |= c.subtreeFlags & 14680064, u |= c.flags & 14680064, c.return = n, c = c.sibling;
    else
      for (c = n.child; c !== null; )
        l |= c.lanes | c.childLanes, u |= c.subtreeFlags, u |= c.flags, c.return = n, c = c.sibling;
    return n.subtreeFlags |= u, n.childLanes = l, r;
  }
  function Dy(n, r, l) {
    var u = r.pendingProps;
    switch (Md(r), r.tag) {
      case 2:
      case 16:
      case 15:
      case 0:
      case 11:
      case 7:
      case 8:
      case 12:
      case 9:
      case 14:
        return Dr(r), null;
      case 1:
        return yn(r.type) && Pa(), Dr(r), null;
      case 3:
        return u = r.stateNode, cu(), Gt(_n), Gt(ot), Hd(), u.pendingContext && (u.context = u.pendingContext, u.pendingContext = null), (n === null || n.child === null) && (Dc(r) ? r.flags |= 4 : n === null || n.memoizedState.isDehydrated && !(r.flags & 256) || (r.flags |= 1024, Ba !== null && (Zd(Ba), Ba = null))), Su(n, r), Dr(r), null;
      case 5:
        Fd(r);
        var c = fo(xs.current);
        if (l = r.type, n !== null && r.stateNode != null)
          xu(n, r, l, u, c), n.ref !== r.ref && (r.flags |= 512, r.flags |= 2097152);
        else {
          if (!u) {
            if (r.stateNode === null)
              throw Error(b(166));
            return Dr(r), null;
          }
          if (n = fo(di.current), Dc(r)) {
            u = r.stateNode, l = r.type;
            var d = r.memoizedProps;
            switch (u[Ei] = r, u[oo] = d, n = (r.mode & 1) !== 0, l) {
              case "dialog":
                sn("cancel", u), sn("close", u);
                break;
              case "iframe":
              case "object":
              case "embed":
                sn("load", u);
                break;
              case "video":
              case "audio":
                for (c = 0; c < fs.length; c++)
                  sn(fs[c], u);
                break;
              case "source":
                sn("error", u);
                break;
              case "img":
              case "image":
              case "link":
                sn(
                  "error",
                  u
                ), sn("load", u);
                break;
              case "details":
                sn("toggle", u);
                break;
              case "input":
                Wn(u, d), sn("invalid", u);
                break;
              case "select":
                u._wrapperState = { wasMultiple: !!d.multiple }, sn("invalid", u);
                break;
              case "textarea":
                Er(u, d), sn("invalid", u);
            }
            Ln(l, d), c = null;
            for (var m in d)
              if (d.hasOwnProperty(m)) {
                var E = d[m];
                m === "children" ? typeof E == "string" ? u.textContent !== E && (d.suppressHydrationWarning !== !0 && Ec(u.textContent, E, n), c = ["children", E]) : typeof E == "number" && u.textContent !== "" + E && (d.suppressHydrationWarning !== !0 && Ec(
                  u.textContent,
                  E,
                  n
                ), c = ["children", "" + E]) : X.hasOwnProperty(m) && E != null && m === "onScroll" && sn("scroll", u);
              }
            switch (l) {
              case "input":
                Fn(u), Gr(u, d, !0);
                break;
              case "textarea":
                Fn(u), sr(u);
                break;
              case "select":
              case "option":
                break;
              default:
                typeof d.onClick == "function" && (u.onclick = wc);
            }
            u = c, r.updateQueue = u, u !== null && (r.flags |= 4);
          } else {
            m = c.nodeType === 9 ? c : c.ownerDocument, n === "http://www.w3.org/1999/xhtml" && (n = Kr(l)), n === "http://www.w3.org/1999/xhtml" ? l === "script" ? (n = m.createElement("div"), n.innerHTML = "<script><\/script>", n = n.removeChild(n.firstChild)) : typeof u.is == "string" ? n = m.createElement(l, { is: u.is }) : (n = m.createElement(l), l === "select" && (m = n, u.multiple ? m.multiple = !0 : u.size && (m.size = u.size))) : n = m.createElementNS(n, l), n[Ei] = r, n[oo] = u, Ti(n, r, !1, !1), r.stateNode = n;
            e: {
              switch (m = Cn(l, u), l) {
                case "dialog":
                  sn("cancel", n), sn("close", n), c = u;
                  break;
                case "iframe":
                case "object":
                case "embed":
                  sn("load", n), c = u;
                  break;
                case "video":
                case "audio":
                  for (c = 0; c < fs.length; c++)
                    sn(fs[c], n);
                  c = u;
                  break;
                case "source":
                  sn("error", n), c = u;
                  break;
                case "img":
                case "image":
                case "link":
                  sn(
                    "error",
                    n
                  ), sn("load", n), c = u;
                  break;
                case "details":
                  sn("toggle", n), c = u;
                  break;
                case "input":
                  Wn(n, u), c = Zn(n, u), sn("invalid", n);
                  break;
                case "option":
                  c = u;
                  break;
                case "select":
                  n._wrapperState = { wasMultiple: !!u.multiple }, c = pe({}, u, { value: void 0 }), sn("invalid", n);
                  break;
                case "textarea":
                  Er(n, u), c = Xr(n, u), sn("invalid", n);
                  break;
                default:
                  c = u;
              }
              Ln(l, c), E = c;
              for (d in E)
                if (E.hasOwnProperty(d)) {
                  var k = E[d];
                  d === "style" ? Qt(n, k) : d === "dangerouslySetInnerHTML" ? (k = k ? k.__html : void 0, k != null && mi(n, k)) : d === "children" ? typeof k == "string" ? (l !== "textarea" || k !== "") && ga(n, k) : typeof k == "number" && ga(n, "" + k) : d !== "suppressContentEditableWarning" && d !== "suppressHydrationWarning" && d !== "autoFocus" && (X.hasOwnProperty(d) ? k != null && d === "onScroll" && sn("scroll", n) : k != null && Ke(n, d, k, m));
                }
              switch (l) {
                case "input":
                  Fn(n), Gr(n, u, !1);
                  break;
                case "textarea":
                  Fn(n), sr(n);
                  break;
                case "option":
                  u.value != null && n.setAttribute("value", "" + St(u.value));
                  break;
                case "select":
                  n.multiple = !!u.multiple, d = u.value, d != null ? Cr(n, !!u.multiple, d, !1) : u.defaultValue != null && Cr(
                    n,
                    !!u.multiple,
                    u.defaultValue,
                    !0
                  );
                  break;
                default:
                  typeof c.onClick == "function" && (n.onclick = wc);
              }
              switch (l) {
                case "button":
                case "input":
                case "select":
                case "textarea":
                  u = !!u.autoFocus;
                  break e;
                case "img":
                  u = !0;
                  break e;
                default:
                  u = !1;
              }
            }
            u && (r.flags |= 4);
          }
          r.ref !== null && (r.flags |= 512, r.flags |= 2097152);
        }
        return Dr(r), null;
      case 6:
        if (n && r.stateNode != null)
          Wa(n, r, n.memoizedProps, u);
        else {
          if (typeof u != "string" && r.stateNode === null)
            throw Error(b(166));
          if (l = fo(xs.current), fo(di.current), Dc(r)) {
            if (u = r.stateNode, l = r.memoizedProps, u[Ei] = r, (d = u.nodeValue !== l) && (n = wa, n !== null))
              switch (n.tag) {
                case 3:
                  Ec(u.nodeValue, l, (n.mode & 1) !== 0);
                  break;
                case 5:
                  n.memoizedProps.suppressHydrationWarning !== !0 && Ec(u.nodeValue, l, (n.mode & 1) !== 0);
              }
            d && (r.flags |= 4);
          } else
            u = (l.nodeType === 9 ? l : l.ownerDocument).createTextNode(u), u[Ei] = r, r.stateNode = u;
        }
        return Dr(r), null;
      case 13:
        if (Gt(gn), u = r.memoizedState, n === null || n.memoizedState !== null && n.memoizedState.dehydrated !== null) {
          if (vn && la !== null && r.mode & 1 && !(r.flags & 128))
            Qv(), wn(), r.flags |= 98560, d = !1;
          else if (d = Dc(r), u !== null && u.dehydrated !== null) {
            if (n === null) {
              if (!d)
                throw Error(b(318));
              if (d = r.memoizedState, d = d !== null ? d.dehydrated : null, !d)
                throw Error(b(317));
              d[Ei] = r;
            } else
              wn(), !(r.flags & 128) && (r.memoizedState = null), r.flags |= 4;
            Dr(r), d = !1;
          } else
            Ba !== null && (Zd(Ba), Ba = null), d = !0;
          if (!d)
            return r.flags & 65536 ? r : null;
        }
        return r.flags & 128 ? (r.lanes = l, r) : (u = u !== null, u !== (n !== null && n.memoizedState !== null) && u && (r.child.flags |= 8192, r.mode & 1 && (n === null || gn.current & 1 ? qn === 0 && (qn = 3) : zs())), r.updateQueue !== null && (r.flags |= 4), Dr(r), null);
      case 4:
        return cu(), Su(n, r), n === null && ru(r.stateNode.containerInfo), Dr(r), null;
      case 10:
        return zd(r.type._context), Dr(r), null;
      case 17:
        return yn(r.type) && Pa(), Dr(r), null;
      case 19:
        if (Gt(gn), d = r.memoizedState, d === null)
          return Dr(r), null;
        if (u = (r.flags & 128) !== 0, m = d.rendering, m === null)
          if (u)
            Dn(d, !1);
          else {
            if (qn !== 0 || n !== null && n.flags & 128)
              for (n = r.child; n !== null; ) {
                if (m = zc(n), m !== null) {
                  for (r.flags |= 128, Dn(d, !1), u = m.updateQueue, u !== null && (r.updateQueue = u, r.flags |= 4), r.subtreeFlags = 0, u = l, l = r.child; l !== null; )
                    d = l, n = u, d.flags &= 14680066, m = d.alternate, m === null ? (d.childLanes = 0, d.lanes = n, d.child = null, d.subtreeFlags = 0, d.memoizedProps = null, d.memoizedState = null, d.updateQueue = null, d.dependencies = null, d.stateNode = null) : (d.childLanes = m.childLanes, d.lanes = m.lanes, d.child = m.child, d.subtreeFlags = 0, d.deletions = null, d.memoizedProps = m.memoizedProps, d.memoizedState = m.memoizedState, d.updateQueue = m.updateQueue, d.type = m.type, n = m.dependencies, d.dependencies = n === null ? null : { lanes: n.lanes, firstContext: n.firstContext }), l = l.sibling;
                  return Zt(gn, gn.current & 1 | 2), r.child;
                }
                n = n.sibling;
              }
            d.tail !== null && Vt() > Nu && (r.flags |= 128, u = !0, Dn(d, !1), r.lanes = 4194304);
          }
        else {
          if (!u)
            if (n = zc(m), n !== null) {
              if (r.flags |= 128, u = !0, l = n.updateQueue, l !== null && (r.updateQueue = l, r.flags |= 4), Dn(d, !0), d.tail === null && d.tailMode === "hidden" && !m.alternate && !vn)
                return Dr(r), null;
            } else
              2 * Vt() - d.renderingStartTime > Nu && l !== 1073741824 && (r.flags |= 128, u = !0, Dn(d, !1), r.lanes = 4194304);
          d.isBackwards ? (m.sibling = r.child, r.child = m) : (l = d.last, l !== null ? l.sibling = m : r.child = m, d.last = m);
        }
        return d.tail !== null ? (r = d.tail, d.rendering = r, d.tail = r.sibling, d.renderingStartTime = Vt(), r.sibling = null, l = gn.current, Zt(gn, u ? l & 1 | 2 : l & 1), r) : (Dr(r), null);
      case 22:
      case 23:
        return hf(), u = r.memoizedState !== null, n !== null && n.memoizedState !== null !== u && (r.flags |= 8192), u && r.mode & 1 ? fa & 1073741824 && (Dr(r), r.subtreeFlags & 6 && (r.flags |= 8192)) : Dr(r), null;
      case 24:
        return null;
      case 25:
        return null;
    }
    throw Error(b(156, r.tag));
  }
  function Ny(n, r) {
    switch (Md(r), r.tag) {
      case 1:
        return yn(r.type) && Pa(), n = r.flags, n & 65536 ? (r.flags = n & -65537 | 128, r) : null;
      case 3:
        return cu(), Gt(_n), Gt(ot), Hd(), n = r.flags, n & 65536 && !(n & 128) ? (r.flags = n & -65537 | 128, r) : null;
      case 5:
        return Fd(r), null;
      case 13:
        if (Gt(gn), n = r.memoizedState, n !== null && n.dehydrated !== null) {
          if (r.alternate === null)
            throw Error(b(340));
          wn();
        }
        return n = r.flags, n & 65536 ? (r.flags = n & -65537 | 128, r) : null;
      case 19:
        return Gt(gn), null;
      case 4:
        return cu(), null;
      case 10:
        return zd(r.type._context), null;
      case 22:
      case 23:
        return hf(), null;
      case 24:
        return null;
      default:
        return null;
    }
  }
  var bu = !1, dr = !1, af = typeof WeakSet == "function" ? WeakSet : Set, Te = null;
  function Cu(n, r) {
    var l = n.ref;
    if (l !== null)
      if (typeof l == "function")
        try {
          l(null);
        } catch (u) {
          On(n, r, u);
        }
      else
        l.current = null;
  }
  function Qd(n, r, l) {
    try {
      l();
    } catch (u) {
      On(n, r, u);
    }
  }
  var lf = !1;
  function Oy(n, r) {
    if (wd = Aa, n = gc(), Ii(n)) {
      if ("selectionStart" in n)
        var l = { start: n.selectionStart, end: n.selectionEnd };
      else
        e: {
          l = (l = n.ownerDocument) && l.defaultView || window;
          var u = l.getSelection && l.getSelection();
          if (u && u.rangeCount !== 0) {
            l = u.anchorNode;
            var c = u.anchorOffset, d = u.focusNode;
            u = u.focusOffset;
            try {
              l.nodeType, d.nodeType;
            } catch {
              l = null;
              break e;
            }
            var m = 0, E = -1, k = -1, H = 0, re = 0, ae = n, te = null;
            t:
              for (; ; ) {
                for (var Ce; ae !== l || c !== 0 && ae.nodeType !== 3 || (E = m + c), ae !== d || u !== 0 && ae.nodeType !== 3 || (k = m + u), ae.nodeType === 3 && (m += ae.nodeValue.length), (Ce = ae.firstChild) !== null; )
                  te = ae, ae = Ce;
                for (; ; ) {
                  if (ae === n)
                    break t;
                  if (te === l && ++H === c && (E = m), te === d && ++re === u && (k = m), (Ce = ae.nextSibling) !== null)
                    break;
                  ae = te, te = ae.parentNode;
                }
                ae = Ce;
              }
            l = E === -1 || k === -1 ? null : { start: E, end: k };
          } else
            l = null;
        }
      l = l || { start: 0, end: 0 };
    } else
      l = null;
    for (io = { focusedElem: n, selectionRange: l }, Aa = !1, Te = r; Te !== null; )
      if (r = Te, n = r.child, (r.subtreeFlags & 1028) !== 0 && n !== null)
        n.return = r, Te = n;
      else
        for (; Te !== null; ) {
          r = Te;
          try {
            var _e = r.alternate;
            if (r.flags & 1024)
              switch (r.tag) {
                case 0:
                case 11:
                case 15:
                  break;
                case 1:
                  if (_e !== null) {
                    var Le = _e.memoizedProps, An = _e.memoizedState, M = r.stateNode, D = M.getSnapshotBeforeUpdate(r.elementType === r.type ? Le : ua(r.type, Le), An);
                    M.__reactInternalSnapshotBeforeUpdate = D;
                  }
                  break;
                case 3:
                  var z = r.stateNode.containerInfo;
                  z.nodeType === 1 ? z.textContent = "" : z.nodeType === 9 && z.documentElement && z.removeChild(z.documentElement);
                  break;
                case 5:
                case 6:
                case 4:
                case 17:
                  break;
                default:
                  throw Error(b(163));
              }
          } catch (se) {
            On(r, r.return, se);
          }
          if (n = r.sibling, n !== null) {
            n.return = r.return, Te = n;
            break;
          }
          Te = r.return;
        }
    return _e = lf, lf = !1, _e;
  }
  function Eu(n, r, l) {
    var u = r.updateQueue;
    if (u = u !== null ? u.lastEffect : null, u !== null) {
      var c = u = u.next;
      do {
        if ((c.tag & n) === n) {
          var d = c.destroy;
          c.destroy = void 0, d !== void 0 && Qd(r, l, d);
        }
        c = c.next;
      } while (c !== u);
    }
  }
  function of(n, r) {
    if (r = r.updateQueue, r = r !== null ? r.lastEffect : null, r !== null) {
      var l = r = r.next;
      do {
        if ((l.tag & n) === n) {
          var u = l.create;
          l.destroy = u();
        }
        l = l.next;
      } while (l !== r);
    }
  }
  function uf(n) {
    var r = n.ref;
    if (r !== null) {
      var l = n.stateNode;
      switch (n.tag) {
        case 5:
          n = l;
          break;
        default:
          n = l;
      }
      typeof r == "function" ? r(n) : r.current = n;
    }
  }
  function dh(n) {
    var r = n.alternate;
    r !== null && (n.alternate = null, dh(r)), n.child = null, n.deletions = null, n.sibling = null, n.tag === 5 && (r = n.stateNode, r !== null && (delete r[Ei], delete r[oo], delete r[kd], delete r[Ry], delete r[_d])), n.stateNode = null, n.return = null, n.dependencies = null, n.memoizedProps = null, n.memoizedState = null, n.pendingProps = null, n.stateNode = null, n.updateQueue = null;
  }
  function Gd(n) {
    return n.tag === 5 || n.tag === 3 || n.tag === 4;
  }
  function ph(n) {
    e:
      for (; ; ) {
        for (; n.sibling === null; ) {
          if (n.return === null || Gd(n.return))
            return null;
          n = n.return;
        }
        for (n.sibling.return = n.return, n = n.sibling; n.tag !== 5 && n.tag !== 6 && n.tag !== 18; ) {
          if (n.flags & 2 || n.child === null || n.tag === 4)
            continue e;
          n.child.return = n, n = n.child;
        }
        if (!(n.flags & 2))
          return n.stateNode;
      }
  }
  function Os(n, r, l) {
    var u = n.tag;
    if (u === 5 || u === 6)
      n = n.stateNode, r ? l.nodeType === 8 ? l.parentNode.insertBefore(n, r) : l.insertBefore(n, r) : (l.nodeType === 8 ? (r = l.parentNode, r.insertBefore(n, l)) : (r = l, r.appendChild(n)), l = l._reactRootContainer, l != null || r.onclick !== null || (r.onclick = wc));
    else if (u !== 4 && (n = n.child, n !== null))
      for (Os(n, r, l), n = n.sibling; n !== null; )
        Os(n, r, l), n = n.sibling;
  }
  function wu(n, r, l) {
    var u = n.tag;
    if (u === 5 || u === 6)
      n = n.stateNode, r ? l.insertBefore(n, r) : l.appendChild(n);
    else if (u !== 4 && (n = n.child, n !== null))
      for (wu(n, r, l), n = n.sibling; n !== null; )
        wu(n, r, l), n = n.sibling;
  }
  var Sn = null, ir = !1;
  function Fr(n, r, l) {
    for (l = l.child; l !== null; )
      Ru(n, r, l), l = l.sibling;
  }
  function Ru(n, r, l) {
    if (Jr && typeof Jr.onCommitFiberUnmount == "function")
      try {
        Jr.onCommitFiberUnmount(ml, l);
      } catch {
      }
    switch (l.tag) {
      case 5:
        dr || Cu(l, r);
      case 6:
        var u = Sn, c = ir;
        Sn = null, Fr(n, r, l), Sn = u, ir = c, Sn !== null && (ir ? (n = Sn, l = l.stateNode, n.nodeType === 8 ? n.parentNode.removeChild(l) : n.removeChild(l)) : Sn.removeChild(l.stateNode));
        break;
      case 18:
        Sn !== null && (ir ? (n = Sn, l = l.stateNode, n.nodeType === 8 ? kl(n.parentNode, l) : n.nodeType === 1 && kl(n, l), El(n)) : kl(Sn, l.stateNode));
        break;
      case 4:
        u = Sn, c = ir, Sn = l.stateNode.containerInfo, ir = !0, Fr(n, r, l), Sn = u, ir = c;
        break;
      case 0:
      case 11:
      case 14:
      case 15:
        if (!dr && (u = l.updateQueue, u !== null && (u = u.lastEffect, u !== null))) {
          c = u = u.next;
          do {
            var d = c, m = d.destroy;
            d = d.tag, m !== void 0 && (d & 2 || d & 4) && Qd(l, r, m), c = c.next;
          } while (c !== u);
        }
        Fr(n, r, l);
        break;
      case 1:
        if (!dr && (Cu(l, r), u = l.stateNode, typeof u.componentWillUnmount == "function"))
          try {
            u.props = l.memoizedProps, u.state = l.memoizedState, u.componentWillUnmount();
          } catch (E) {
            On(l, r, E);
          }
        Fr(n, r, l);
        break;
      case 21:
        Fr(n, r, l);
        break;
      case 22:
        l.mode & 1 ? (dr = (u = dr) || l.memoizedState !== null, Fr(n, r, l), dr = u) : Fr(n, r, l);
        break;
      default:
        Fr(n, r, l);
    }
  }
  function Tu(n) {
    var r = n.updateQueue;
    if (r !== null) {
      n.updateQueue = null;
      var l = n.stateNode;
      l === null && (l = n.stateNode = new af()), r.forEach(function(u) {
        var c = Fy.bind(null, n, u);
        l.has(u) || (l.add(u), u.then(c, c));
      });
    }
  }
  function lr(n, r) {
    var l = r.deletions;
    if (l !== null)
      for (var u = 0; u < l.length; u++) {
        var c = l[u];
        try {
          var d = n, m = r, E = m;
          e:
            for (; E !== null; ) {
              switch (E.tag) {
                case 5:
                  Sn = E.stateNode, ir = !1;
                  break e;
                case 3:
                  Sn = E.stateNode.containerInfo, ir = !0;
                  break e;
                case 4:
                  Sn = E.stateNode.containerInfo, ir = !0;
                  break e;
              }
              E = E.return;
            }
          if (Sn === null)
            throw Error(b(160));
          Ru(d, m, c), Sn = null, ir = !1;
          var k = c.alternate;
          k !== null && (k.return = null), c.return = null;
        } catch (H) {
          On(c, r, H);
        }
      }
    if (r.subtreeFlags & 12854)
      for (r = r.child; r !== null; )
        vh(r, n), r = r.sibling;
  }
  function vh(n, r) {
    var l = n.alternate, u = n.flags;
    switch (n.tag) {
      case 0:
      case 11:
      case 14:
      case 15:
        if (lr(r, n), ki(n), u & 4) {
          try {
            Eu(3, n, n.return), of(3, n);
          } catch (Le) {
            On(n, n.return, Le);
          }
          try {
            Eu(5, n, n.return);
          } catch (Le) {
            On(n, n.return, Le);
          }
        }
        break;
      case 1:
        lr(r, n), ki(n), u & 512 && l !== null && Cu(l, l.return);
        break;
      case 5:
        if (lr(r, n), ki(n), u & 512 && l !== null && Cu(l, l.return), n.flags & 32) {
          var c = n.stateNode;
          try {
            ga(c, "");
          } catch (Le) {
            On(n, n.return, Le);
          }
        }
        if (u & 4 && (c = n.stateNode, c != null)) {
          var d = n.memoizedProps, m = l !== null ? l.memoizedProps : d, E = n.type, k = n.updateQueue;
          if (n.updateQueue = null, k !== null)
            try {
              E === "input" && d.type === "radio" && d.name != null && Hn(c, d), Cn(E, m);
              var H = Cn(E, d);
              for (m = 0; m < k.length; m += 2) {
                var re = k[m], ae = k[m + 1];
                re === "style" ? Qt(c, ae) : re === "dangerouslySetInnerHTML" ? mi(c, ae) : re === "children" ? ga(c, ae) : Ke(c, re, ae, H);
              }
              switch (E) {
                case "input":
                  Mn(c, d);
                  break;
                case "textarea":
                  ya(c, d);
                  break;
                case "select":
                  var te = c._wrapperState.wasMultiple;
                  c._wrapperState.wasMultiple = !!d.multiple;
                  var Ce = d.value;
                  Ce != null ? Cr(c, !!d.multiple, Ce, !1) : te !== !!d.multiple && (d.defaultValue != null ? Cr(
                    c,
                    !!d.multiple,
                    d.defaultValue,
                    !0
                  ) : Cr(c, !!d.multiple, d.multiple ? [] : "", !1));
              }
              c[oo] = d;
            } catch (Le) {
              On(n, n.return, Le);
            }
        }
        break;
      case 6:
        if (lr(r, n), ki(n), u & 4) {
          if (n.stateNode === null)
            throw Error(b(162));
          c = n.stateNode, d = n.memoizedProps;
          try {
            c.nodeValue = d;
          } catch (Le) {
            On(n, n.return, Le);
          }
        }
        break;
      case 3:
        if (lr(r, n), ki(n), u & 4 && l !== null && l.memoizedState.isDehydrated)
          try {
            El(r.containerInfo);
          } catch (Le) {
            On(n, n.return, Le);
          }
        break;
      case 4:
        lr(r, n), ki(n);
        break;
      case 13:
        lr(r, n), ki(n), c = n.child, c.flags & 8192 && (d = c.memoizedState !== null, c.stateNode.isHidden = d, !d || c.alternate !== null && c.alternate.memoizedState !== null || (cf = Vt())), u & 4 && Tu(n);
        break;
      case 22:
        if (re = l !== null && l.memoizedState !== null, n.mode & 1 ? (dr = (H = dr) || re, lr(r, n), dr = H) : lr(r, n), ki(n), u & 8192) {
          if (H = n.memoizedState !== null, (n.stateNode.isHidden = H) && !re && n.mode & 1)
            for (Te = n, re = n.child; re !== null; ) {
              for (ae = Te = re; Te !== null; ) {
                switch (te = Te, Ce = te.child, te.tag) {
                  case 0:
                  case 11:
                  case 14:
                  case 15:
                    Eu(4, te, te.return);
                    break;
                  case 1:
                    Cu(te, te.return);
                    var _e = te.stateNode;
                    if (typeof _e.componentWillUnmount == "function") {
                      u = te, l = te.return;
                      try {
                        r = u, _e.props = r.memoizedProps, _e.state = r.memoizedState, _e.componentWillUnmount();
                      } catch (Le) {
                        On(u, l, Le);
                      }
                    }
                    break;
                  case 5:
                    Cu(te, te.return);
                    break;
                  case 22:
                    if (te.memoizedState !== null) {
                      hh(ae);
                      continue;
                    }
                }
                Ce !== null ? (Ce.return = te, Te = Ce) : hh(ae);
              }
              re = re.sibling;
            }
          e:
            for (re = null, ae = n; ; ) {
              if (ae.tag === 5) {
                if (re === null) {
                  re = ae;
                  try {
                    c = ae.stateNode, H ? (d = c.style, typeof d.setProperty == "function" ? d.setProperty("display", "none", "important") : d.display = "none") : (E = ae.stateNode, k = ae.memoizedProps.style, m = k != null && k.hasOwnProperty("display") ? k.display : null, E.style.display = bt("display", m));
                  } catch (Le) {
                    On(n, n.return, Le);
                  }
                }
              } else if (ae.tag === 6) {
                if (re === null)
                  try {
                    ae.stateNode.nodeValue = H ? "" : ae.memoizedProps;
                  } catch (Le) {
                    On(n, n.return, Le);
                  }
              } else if ((ae.tag !== 22 && ae.tag !== 23 || ae.memoizedState === null || ae === n) && ae.child !== null) {
                ae.child.return = ae, ae = ae.child;
                continue;
              }
              if (ae === n)
                break e;
              for (; ae.sibling === null; ) {
                if (ae.return === null || ae.return === n)
                  break e;
                re === ae && (re = null), ae = ae.return;
              }
              re === ae && (re = null), ae.sibling.return = ae.return, ae = ae.sibling;
            }
        }
        break;
      case 19:
        lr(r, n), ki(n), u & 4 && Tu(n);
        break;
      case 21:
        break;
      default:
        lr(
          r,
          n
        ), ki(n);
    }
  }
  function ki(n) {
    var r = n.flags;
    if (r & 2) {
      try {
        e: {
          for (var l = n.return; l !== null; ) {
            if (Gd(l)) {
              var u = l;
              break e;
            }
            l = l.return;
          }
          throw Error(b(160));
        }
        switch (u.tag) {
          case 5:
            var c = u.stateNode;
            u.flags & 32 && (ga(c, ""), u.flags &= -33);
            var d = ph(n);
            wu(n, d, c);
            break;
          case 3:
          case 4:
            var m = u.stateNode.containerInfo, E = ph(n);
            Os(n, E, m);
            break;
          default:
            throw Error(b(161));
        }
      } catch (k) {
        On(n, n.return, k);
      }
      n.flags &= -3;
    }
    r & 4096 && (n.flags &= -4097);
  }
  function My(n, r, l) {
    Te = n, qd(n);
  }
  function qd(n, r, l) {
    for (var u = (n.mode & 1) !== 0; Te !== null; ) {
      var c = Te, d = c.child;
      if (c.tag === 22 && u) {
        var m = c.memoizedState !== null || bu;
        if (!m) {
          var E = c.alternate, k = E !== null && E.memoizedState !== null || dr;
          E = bu;
          var H = dr;
          if (bu = m, (dr = k) && !H)
            for (Te = c; Te !== null; )
              m = Te, k = m.child, m.tag === 22 && m.memoizedState !== null ? Xd(c) : k !== null ? (k.return = m, Te = k) : Xd(c);
          for (; d !== null; )
            Te = d, qd(d), d = d.sibling;
          Te = c, bu = E, dr = H;
        }
        ku(n);
      } else
        c.subtreeFlags & 8772 && d !== null ? (d.return = c, Te = d) : ku(n);
    }
  }
  function ku(n) {
    for (; Te !== null; ) {
      var r = Te;
      if (r.flags & 8772) {
        var l = r.alternate;
        try {
          if (r.flags & 8772)
            switch (r.tag) {
              case 0:
              case 11:
              case 15:
                dr || of(5, r);
                break;
              case 1:
                var u = r.stateNode;
                if (r.flags & 4 && !dr)
                  if (l === null)
                    u.componentDidMount();
                  else {
                    var c = r.elementType === r.type ? l.memoizedProps : ua(r.type, l.memoizedProps);
                    u.componentDidUpdate(c, l.memoizedState, u.__reactInternalSnapshotBeforeUpdate);
                  }
                var d = r.updateQueue;
                d !== null && Jv(r, d, u);
                break;
              case 3:
                var m = r.updateQueue;
                if (m !== null) {
                  if (l = null, r.child !== null)
                    switch (r.child.tag) {
                      case 5:
                        l = r.child.stateNode;
                        break;
                      case 1:
                        l = r.child.stateNode;
                    }
                  Jv(r, m, l);
                }
                break;
              case 5:
                var E = r.stateNode;
                if (l === null && r.flags & 4) {
                  l = E;
                  var k = r.memoizedProps;
                  switch (r.type) {
                    case "button":
                    case "input":
                    case "select":
                    case "textarea":
                      k.autoFocus && l.focus();
                      break;
                    case "img":
                      k.src && (l.src = k.src);
                  }
                }
                break;
              case 6:
                break;
              case 4:
                break;
              case 12:
                break;
              case 13:
                if (r.memoizedState === null) {
                  var H = r.alternate;
                  if (H !== null) {
                    var re = H.memoizedState;
                    if (re !== null) {
                      var ae = re.dehydrated;
                      ae !== null && El(ae);
                    }
                  }
                }
                break;
              case 19:
              case 17:
              case 21:
              case 22:
              case 23:
              case 25:
                break;
              default:
                throw Error(b(163));
            }
          dr || r.flags & 512 && uf(r);
        } catch (te) {
          On(r, r.return, te);
        }
      }
      if (r === n) {
        Te = null;
        break;
      }
      if (l = r.sibling, l !== null) {
        l.return = r.return, Te = l;
        break;
      }
      Te = r.return;
    }
  }
  function hh(n) {
    for (; Te !== null; ) {
      var r = Te;
      if (r === n) {
        Te = null;
        break;
      }
      var l = r.sibling;
      if (l !== null) {
        l.return = r.return, Te = l;
        break;
      }
      Te = r.return;
    }
  }
  function Xd(n) {
    for (; Te !== null; ) {
      var r = Te;
      try {
        switch (r.tag) {
          case 0:
          case 11:
          case 15:
            var l = r.return;
            try {
              of(4, r);
            } catch (k) {
              On(r, l, k);
            }
            break;
          case 1:
            var u = r.stateNode;
            if (typeof u.componentDidMount == "function") {
              var c = r.return;
              try {
                u.componentDidMount();
              } catch (k) {
                On(r, c, k);
              }
            }
            var d = r.return;
            try {
              uf(r);
            } catch (k) {
              On(r, d, k);
            }
            break;
          case 5:
            var m = r.return;
            try {
              uf(r);
            } catch (k) {
              On(r, m, k);
            }
        }
      } catch (k) {
        On(r, r.return, k);
      }
      if (r === n) {
        Te = null;
        break;
      }
      var E = r.sibling;
      if (E !== null) {
        E.return = r.return, Te = E;
        break;
      }
      Te = r.return;
    }
  }
  var Ly = Math.ceil, xo = ct.ReactCurrentDispatcher, sf = ct.ReactCurrentOwner, Qa = ct.ReactCurrentBatchConfig, Ot = 0, Nn = null, hn = null, Gn = 0, fa = 0, _u = xt(0), qn = 0, Ms = null, bo = 0, Du = 0, Kd = 0, Ul = null, Nr = null, cf = 0, Nu = 1 / 0, Zi = null, ff = !1, Jd = null, Ga = null, Ou = !1, qa = null, df = 0, Ls = 0, pf = null, js = -1, Co = 0;
  function or() {
    return Ot & 6 ? Vt() : js !== -1 ? js : js = Vt();
  }
  function el(n) {
    return n.mode & 1 ? Ot & 2 && Gn !== 0 ? Gn & -Gn : Nc.transition !== null ? (Co === 0 && (Co = $o()), Co) : (n = Bt, n !== 0 || (n = window.event, n = n === void 0 ? 16 : ns(n.type)), n) : 1;
  }
  function Rn(n, r, l, u) {
    if (50 < Ls)
      throw Ls = 0, pf = null, Error(b(185));
    Fi(n, l, u), (!(Ot & 2) || n !== Nn) && (n === Nn && (!(Ot & 2) && (Du |= l), qn === 4 && _i(n, Gn)), Xn(n, u), l === 1 && Ot === 0 && !(r.mode & 1) && (Nu = Vt() + 500, ar && ra()));
  }
  function Xn(n, r) {
    var l = n.callbackNode;
    Sl(n, r);
    var u = Ar(n, n === Nn ? Gn : 0);
    if (u === 0)
      l !== null && dn(l), n.callbackNode = null, n.callbackPriority = 0;
    else if (r = u & -u, n.callbackPriority !== r) {
      if (l != null && dn(l), r === 1)
        n.tag === 0 ? Nd(Mu.bind(null, n)) : Dd(Mu.bind(null, n)), Td(function() {
          !(Ot & 6) && ra();
        }), l = null;
      else {
        switch (Yo(u)) {
          case 1:
            l = jr;
            break;
          case 4:
            l = Et;
            break;
          case 16:
            l = ja;
            break;
          case 536870912:
            l = Vo;
            break;
          default:
            l = ja;
        }
        l = Eh(l, vf.bind(null, n));
      }
      n.callbackPriority = r, n.callbackNode = l;
    }
  }
  function vf(n, r) {
    if (js = -1, Co = 0, Ot & 6)
      throw Error(b(327));
    var l = n.callbackNode;
    if (Lu() && n.callbackNode !== l)
      return null;
    var u = Ar(n, n === Nn ? Gn : 0);
    if (u === 0)
      return null;
    if (u & 30 || u & n.expiredLanes || r)
      r = mf(n, u);
    else {
      r = u;
      var c = Ot;
      Ot |= 2;
      var d = yh();
      (Nn !== n || Gn !== r) && (Zi = null, Nu = Vt() + 500, wo(n, r));
      do
        try {
          zy();
          break;
        } catch (E) {
          mh(n, E);
        }
      while (1);
      Ra(), xo.current = d, Ot = c, hn !== null ? r = 0 : (Nn = null, Gn = 0, r = qn);
    }
    if (r !== 0) {
      if (r === 2 && (c = xl(n), c !== 0 && (u = c, r = Eo(n, c))), r === 1)
        throw l = Ms, wo(n, 0), _i(n, u), Xn(n, Vt()), l;
      if (r === 6)
        _i(n, u);
      else {
        if (c = n.current.alternate, !(u & 30) && !ep(c) && (r = mf(n, u), r === 2 && (d = xl(n), d !== 0 && (u = d, r = Eo(n, d))), r === 1))
          throw l = Ms, wo(n, 0), _i(n, u), Xn(n, Vt()), l;
        switch (n.finishedWork = c, n.finishedLanes = u, r) {
          case 0:
          case 1:
            throw Error(b(345));
          case 2:
            Fl(n, Nr, Zi);
            break;
          case 3:
            if (_i(n, u), (u & 130023424) === u && (r = cf + 500 - Vt(), 10 < r)) {
              if (Ar(n, 0) !== 0)
                break;
              if (c = n.suspendedLanes, (c & u) !== u) {
                or(), n.pingedLanes |= n.suspendedLanes & c;
                break;
              }
              n.timeoutHandle = lo(Fl.bind(null, n, Nr, Zi), r);
              break;
            }
            Fl(n, Nr, Zi);
            break;
          case 4:
            if (_i(n, u), (u & 4194240) === u)
              break;
            for (r = n.eventTimes, c = -1; 0 < u; ) {
              var m = 31 - zr(u);
              d = 1 << m, m = r[m], m > c && (c = m), u &= ~d;
            }
            if (u = c, u = Vt() - u, u = (120 > u ? 120 : 480 > u ? 480 : 1080 > u ? 1080 : 1920 > u ? 1920 : 3e3 > u ? 3e3 : 4320 > u ? 4320 : 1960 * Ly(u / 1960)) - u, 10 < u) {
              n.timeoutHandle = lo(Fl.bind(null, n, Nr, Zi), u);
              break;
            }
            Fl(n, Nr, Zi);
            break;
          case 5:
            Fl(n, Nr, Zi);
            break;
          default:
            throw Error(b(329));
        }
      }
    }
    return Xn(n, Vt()), n.callbackNode === l ? vf.bind(null, n) : null;
  }
  function Eo(n, r) {
    var l = Ul;
    return n.current.memoizedState.isDehydrated && (wo(n, r).flags |= 256), n = mf(n, r), n !== 2 && (r = Nr, Nr = l, r !== null && Zd(r)), n;
  }
  function Zd(n) {
    Nr === null ? Nr = n : Nr.push.apply(Nr, n);
  }
  function ep(n) {
    for (var r = n; ; ) {
      if (r.flags & 16384) {
        var l = r.updateQueue;
        if (l !== null && (l = l.stores, l !== null))
          for (var u = 0; u < l.length; u++) {
            var c = l[u], d = c.getSnapshot;
            c = c.value;
            try {
              if (!Ua(d(), c))
                return !1;
            } catch {
              return !1;
            }
          }
      }
      if (l = r.child, r.subtreeFlags & 16384 && l !== null)
        l.return = r, r = l;
      else {
        if (r === n)
          break;
        for (; r.sibling === null; ) {
          if (r.return === null || r.return === n)
            return !0;
          r = r.return;
        }
        r.sibling.return = r.return, r = r.sibling;
      }
    }
    return !0;
  }
  function _i(n, r) {
    for (r &= ~Kd, r &= ~Du, n.suspendedLanes |= r, n.pingedLanes &= ~r, n = n.expirationTimes; 0 < r; ) {
      var l = 31 - zr(r), u = 1 << l;
      n[l] = -1, r &= ~u;
    }
  }
  function Mu(n) {
    if (Ot & 6)
      throw Error(b(327));
    Lu();
    var r = Ar(n, 0);
    if (!(r & 1))
      return Xn(n, Vt()), null;
    var l = mf(n, r);
    if (n.tag !== 0 && l === 2) {
      var u = xl(n);
      u !== 0 && (r = u, l = Eo(n, u));
    }
    if (l === 1)
      throw l = Ms, wo(n, 0), _i(n, r), Xn(n, Vt()), l;
    if (l === 6)
      throw Error(b(345));
    return n.finishedWork = n.current.alternate, n.finishedLanes = r, Fl(n, Nr, Zi), Xn(n, Vt()), null;
  }
  function tp(n, r) {
    var l = Ot;
    Ot |= 1;
    try {
      return n(r);
    } finally {
      Ot = l, Ot === 0 && (Nu = Vt() + 500, ar && ra());
    }
  }
  function Di(n) {
    qa !== null && qa.tag === 0 && !(Ot & 6) && Lu();
    var r = Ot;
    Ot |= 1;
    var l = Qa.transition, u = Bt;
    try {
      if (Qa.transition = null, Bt = 1, n)
        return n();
    } finally {
      Bt = u, Qa.transition = l, Ot = r, !(Ot & 6) && ra();
    }
  }
  function hf() {
    fa = _u.current, Gt(_u);
  }
  function wo(n, r) {
    n.finishedWork = null, n.finishedLanes = 0;
    var l = n.timeoutHandle;
    if (l !== -1 && (n.timeoutHandle = -1, $v(l)), hn !== null)
      for (l = hn.return; l !== null; ) {
        var u = l;
        switch (Md(u), u.tag) {
          case 1:
            u = u.type.childContextTypes, u != null && Pa();
            break;
          case 3:
            cu(), Gt(_n), Gt(ot), Hd();
            break;
          case 5:
            Fd(u);
            break;
          case 4:
            cu();
            break;
          case 13:
            Gt(gn);
            break;
          case 19:
            Gt(gn);
            break;
          case 10:
            zd(u.type._context);
            break;
          case 22:
          case 23:
            hf();
        }
        l = l.return;
      }
    if (Nn = n, hn = n = Hl(n.current, null), Gn = fa = r, qn = 0, Ms = null, Kd = Du = bo = 0, Nr = Ul = null, co !== null) {
      for (r = 0; r < co.length; r++)
        if (l = co[r], u = l.interleaved, u !== null) {
          l.interleaved = null;
          var c = u.next, d = l.pending;
          if (d !== null) {
            var m = d.next;
            d.next = c, u.next = m;
          }
          l.pending = u;
        }
      co = null;
    }
    return n;
  }
  function mh(n, r) {
    do {
      var l = hn;
      try {
        if (Ra(), Uc.current = _r, Ta) {
          for (var u = Ve.memoizedState; u !== null; ) {
            var c = u.queue;
            c !== null && (c.pending = null), u = u.next;
          }
          Ta = !1;
        }
        if (Fe = 0, _t = ut = Ve = null, fu = !1, Cs = 0, sf.current = null, l === null || l.return === null) {
          qn = 1, Ms = r, hn = null;
          break;
        }
        e: {
          var d = n, m = l.return, E = l, k = r;
          if (r = Gn, E.flags |= 32768, k !== null && typeof k == "object" && typeof k.then == "function") {
            var H = k, re = E, ae = re.tag;
            if (!(re.mode & 1) && (ae === 0 || ae === 11 || ae === 15)) {
              var te = re.alternate;
              te ? (re.updateQueue = te.updateQueue, re.memoizedState = te.memoizedState, re.lanes = te.lanes) : (re.updateQueue = null, re.memoizedState = null);
            }
            var Ce = oh(m);
            if (Ce !== null) {
              Ce.flags &= -257, Id(Ce, m, E, d, r), Ce.mode & 1 && ks(d, H, r), r = Ce, k = H;
              var _e = r.updateQueue;
              if (_e === null) {
                var Le = /* @__PURE__ */ new Set();
                Le.add(k), r.updateQueue = Le;
              } else
                _e.add(k);
              break e;
            } else {
              if (!(r & 1)) {
                ks(d, H, r), zs();
                break e;
              }
              k = Error(b(426));
            }
          } else if (vn && E.mode & 1) {
            var An = oh(m);
            if (An !== null) {
              !(An.flags & 65536) && (An.flags |= 256), Id(An, m, E, d, r), jd(zl(k, E));
              break e;
            }
          }
          d = k = zl(k, E), qn !== 4 && (qn = 2), Ul === null ? Ul = [d] : Ul.push(d), d = m;
          do {
            switch (d.tag) {
              case 3:
                d.flags |= 65536, r &= -r, d.lanes |= r;
                var M = ih(d, k, r);
                Kv(d, M);
                break e;
              case 1:
                E = k;
                var D = d.type, z = d.stateNode;
                if (!(d.flags & 128) && (typeof D.getDerivedStateFromError == "function" || z !== null && typeof z.componentDidCatch == "function" && (Ga === null || !Ga.has(z)))) {
                  d.flags |= 65536, r &= -r, d.lanes |= r;
                  var se = lh(d, E, r);
                  Kv(d, se);
                  break e;
                }
            }
            d = d.return;
          } while (d !== null);
        }
        Sh(l);
      } catch (He) {
        r = He, hn === l && l !== null && (hn = l = l.return);
        continue;
      }
      break;
    } while (1);
  }
  function yh() {
    var n = xo.current;
    return xo.current = _r, n === null ? _r : n;
  }
  function zs() {
    (qn === 0 || qn === 3 || qn === 2) && (qn = 4), Nn === null || !(bo & 268435455) && !(Du & 268435455) || _i(Nn, Gn);
  }
  function mf(n, r) {
    var l = Ot;
    Ot |= 2;
    var u = yh();
    (Nn !== n || Gn !== r) && (Zi = null, wo(n, r));
    do
      try {
        jy();
        break;
      } catch (c) {
        mh(n, c);
      }
    while (1);
    if (Ra(), Ot = l, xo.current = u, hn !== null)
      throw Error(b(261));
    return Nn = null, Gn = 0, qn;
  }
  function jy() {
    for (; hn !== null; )
      gh(hn);
  }
  function zy() {
    for (; hn !== null && !Rr(); )
      gh(hn);
  }
  function gh(n) {
    var r = Ch(n.alternate, n, fa);
    n.memoizedProps = n.pendingProps, r === null ? Sh(n) : hn = r, sf.current = null;
  }
  function Sh(n) {
    var r = n;
    do {
      var l = r.alternate;
      if (n = r.return, r.flags & 32768) {
        if (l = Ny(l, r), l !== null) {
          l.flags &= 32767, hn = l;
          return;
        }
        if (n !== null)
          n.flags |= 32768, n.subtreeFlags = 0, n.deletions = null;
        else {
          qn = 6, hn = null;
          return;
        }
      } else if (l = Dy(l, r, fa), l !== null) {
        hn = l;
        return;
      }
      if (r = r.sibling, r !== null) {
        hn = r;
        return;
      }
      hn = r = n;
    } while (r !== null);
    qn === 0 && (qn = 5);
  }
  function Fl(n, r, l) {
    var u = Bt, c = Qa.transition;
    try {
      Qa.transition = null, Bt = 1, Ay(n, r, l, u);
    } finally {
      Qa.transition = c, Bt = u;
    }
    return null;
  }
  function Ay(n, r, l, u) {
    do
      Lu();
    while (qa !== null);
    if (Ot & 6)
      throw Error(b(327));
    l = n.finishedWork;
    var c = n.finishedLanes;
    if (l === null)
      return null;
    if (n.finishedWork = null, n.finishedLanes = 0, l === n.current)
      throw Error(b(177));
    n.callbackNode = null, n.callbackPriority = 0;
    var d = l.lanes | l.childLanes;
    if (id(n, d), n === Nn && (hn = Nn = null, Gn = 0), !(l.subtreeFlags & 2064) && !(l.flags & 2064) || Ou || (Ou = !0, Eh(ja, function() {
      return Lu(), null;
    })), d = (l.flags & 15990) !== 0, l.subtreeFlags & 15990 || d) {
      d = Qa.transition, Qa.transition = null;
      var m = Bt;
      Bt = 1;
      var E = Ot;
      Ot |= 4, sf.current = null, Oy(n, l), vh(l, n), Sc(io), Aa = !!wd, io = wd = null, n.current = l, My(l), xi(), Ot = E, Bt = m, Qa.transition = d;
    } else
      n.current = l;
    if (Ou && (Ou = !1, qa = n, df = c), d = n.pendingLanes, d === 0 && (Ga = null), Zu(l.stateNode), Xn(n, Vt()), r !== null)
      for (u = n.onRecoverableError, l = 0; l < r.length; l++)
        c = r[l], u(c.value, { componentStack: c.stack, digest: c.digest });
    if (ff)
      throw ff = !1, n = Jd, Jd = null, n;
    return df & 1 && n.tag !== 0 && Lu(), d = n.pendingLanes, d & 1 ? n === pf ? Ls++ : (Ls = 0, pf = n) : Ls = 0, ra(), null;
  }
  function Lu() {
    if (qa !== null) {
      var n = Yo(df), r = Qa.transition, l = Bt;
      try {
        if (Qa.transition = null, Bt = 16 > n ? 16 : n, qa === null)
          var u = !1;
        else {
          if (n = qa, qa = null, df = 0, Ot & 6)
            throw Error(b(331));
          var c = Ot;
          for (Ot |= 4, Te = n.current; Te !== null; ) {
            var d = Te, m = d.child;
            if (Te.flags & 16) {
              var E = d.deletions;
              if (E !== null) {
                for (var k = 0; k < E.length; k++) {
                  var H = E[k];
                  for (Te = H; Te !== null; ) {
                    var re = Te;
                    switch (re.tag) {
                      case 0:
                      case 11:
                      case 15:
                        Eu(8, re, d);
                    }
                    var ae = re.child;
                    if (ae !== null)
                      ae.return = re, Te = ae;
                    else
                      for (; Te !== null; ) {
                        re = Te;
                        var te = re.sibling, Ce = re.return;
                        if (dh(re), re === H) {
                          Te = null;
                          break;
                        }
                        if (te !== null) {
                          te.return = Ce, Te = te;
                          break;
                        }
                        Te = Ce;
                      }
                  }
                }
                var _e = d.alternate;
                if (_e !== null) {
                  var Le = _e.child;
                  if (Le !== null) {
                    _e.child = null;
                    do {
                      var An = Le.sibling;
                      Le.sibling = null, Le = An;
                    } while (Le !== null);
                  }
                }
                Te = d;
              }
            }
            if (d.subtreeFlags & 2064 && m !== null)
              m.return = d, Te = m;
            else
              e:
                for (; Te !== null; ) {
                  if (d = Te, d.flags & 2048)
                    switch (d.tag) {
                      case 0:
                      case 11:
                      case 15:
                        Eu(9, d, d.return);
                    }
                  var M = d.sibling;
                  if (M !== null) {
                    M.return = d.return, Te = M;
                    break e;
                  }
                  Te = d.return;
                }
          }
          var D = n.current;
          for (Te = D; Te !== null; ) {
            m = Te;
            var z = m.child;
            if (m.subtreeFlags & 2064 && z !== null)
              z.return = m, Te = z;
            else
              e:
                for (m = D; Te !== null; ) {
                  if (E = Te, E.flags & 2048)
                    try {
                      switch (E.tag) {
                        case 0:
                        case 11:
                        case 15:
                          of(9, E);
                      }
                    } catch (He) {
                      On(E, E.return, He);
                    }
                  if (E === m) {
                    Te = null;
                    break e;
                  }
                  var se = E.sibling;
                  if (se !== null) {
                    se.return = E.return, Te = se;
                    break e;
                  }
                  Te = E.return;
                }
          }
          if (Ot = c, ra(), Jr && typeof Jr.onPostCommitFiberRoot == "function")
            try {
              Jr.onPostCommitFiberRoot(ml, n);
            } catch {
            }
          u = !0;
        }
        return u;
      } finally {
        Bt = l, Qa.transition = r;
      }
    }
    return !1;
  }
  function xh(n, r, l) {
    r = zl(l, r), r = ih(n, r, 1), n = Ll(n, r, 1), r = or(), n !== null && (Fi(n, 1, r), Xn(n, r));
  }
  function On(n, r, l) {
    if (n.tag === 3)
      xh(n, n, l);
    else
      for (; r !== null; ) {
        if (r.tag === 3) {
          xh(r, n, l);
          break;
        } else if (r.tag === 1) {
          var u = r.stateNode;
          if (typeof r.type.getDerivedStateFromError == "function" || typeof u.componentDidCatch == "function" && (Ga === null || !Ga.has(u))) {
            n = zl(l, n), n = lh(r, n, 1), r = Ll(r, n, 1), n = or(), r !== null && (Fi(r, 1, n), Xn(r, n));
            break;
          }
        }
        r = r.return;
      }
  }
  function Uy(n, r, l) {
    var u = n.pingCache;
    u !== null && u.delete(r), r = or(), n.pingedLanes |= n.suspendedLanes & l, Nn === n && (Gn & l) === l && (qn === 4 || qn === 3 && (Gn & 130023424) === Gn && 500 > Vt() - cf ? wo(n, 0) : Kd |= l), Xn(n, r);
  }
  function bh(n, r) {
    r === 0 && (n.mode & 1 ? (r = yl, yl <<= 1, !(yl & 130023424) && (yl = 4194304)) : r = 1);
    var l = or();
    n = Xi(n, r), n !== null && (Fi(n, r, l), Xn(n, l));
  }
  function np(n) {
    var r = n.memoizedState, l = 0;
    r !== null && (l = r.retryLane), bh(n, l);
  }
  function Fy(n, r) {
    var l = 0;
    switch (n.tag) {
      case 13:
        var u = n.stateNode, c = n.memoizedState;
        c !== null && (l = c.retryLane);
        break;
      case 19:
        u = n.stateNode;
        break;
      default:
        throw Error(b(314));
    }
    u !== null && u.delete(r), bh(n, l);
  }
  var Ch;
  Ch = function(n, r, l) {
    if (n !== null)
      if (n.memoizedProps !== r.pendingProps || _n.current)
        sa = !0;
      else {
        if (!(n.lanes & l) && !(r.flags & 128))
          return sa = !1, Ji(n, r, l);
        sa = !!(n.flags & 131072);
      }
    else
      sa = !1, vn && r.flags & 1048576 && Od(r, iu, r.index);
    switch (r.lanes = 0, r.tag) {
      case 2:
        var u = r.type;
        Ns(n, r), n = r.pendingProps;
        var c = Ha(r, ot.current);
        ou(r, l), c = Z(null, r, u, n, c, l);
        var d = $n();
        return r.flags |= 1, typeof c == "object" && c !== null && typeof c.render == "function" && c.$$typeof === void 0 ? (r.tag = 1, r.memoizedState = null, r.updateQueue = null, yn(u) ? (d = !0, Rc(r)) : d = !1, r.memoizedState = c.state !== null && c.state !== void 0 ? c.state : null, Mc(r), c.updater = yo, r.stateNode = c, c._reactInternals = r, Bd(r, u, n, l), r = ef(null, r, u, !0, d, l)) : (r.tag = 0, vn && d && Tc(r), jn(null, r, c, l), r = r.child), r;
      case 16:
        u = r.elementType;
        e: {
          switch (Ns(n, r), n = r.pendingProps, c = u._init, u = c(u._payload), r.type = u, c = r.tag = Hy(u), n = ua(u, n), c) {
            case 0:
              r = gt(null, r, u, n, l);
              break e;
            case 1:
              r = _s(null, r, u, n, l);
              break e;
            case 11:
              r = gu(null, r, u, n, l);
              break e;
            case 14:
              r = Al(null, r, u, ua(u.type, n), l);
              break e;
          }
          throw Error(b(
            306,
            u,
            ""
          ));
        }
        return r;
      case 0:
        return u = r.type, c = r.pendingProps, c = r.elementType === u ? c : ua(u, c), gt(n, r, u, c, l);
      case 1:
        return u = r.type, c = r.pendingProps, c = r.elementType === u ? c : ua(u, c), _s(n, r, u, c, l);
      case 3:
        e: {
          if (_y(r), n === null)
            throw Error(b(387));
          u = r.pendingProps, d = r.memoizedState, c = d.element, uu(n, r), jc(r, u, null, l);
          var m = r.memoizedState;
          if (u = m.element, d.isDehydrated)
            if (d = { element: u, isDehydrated: !1, cache: m.cache, pendingSuspenseBoundaries: m.pendingSuspenseBoundaries, transitions: m.transitions }, r.updateQueue.baseState = d, r.memoizedState = d, r.flags & 256) {
              c = zl(Error(b(423)), r), r = sh(n, r, u, l, c);
              break e;
            } else if (u !== c) {
              c = zl(Error(b(424)), r), r = sh(n, r, u, l, c);
              break e;
            } else
              for (la = fi(r.stateNode.containerInfo.firstChild), wa = r, vn = !0, Ba = null, l = qv(r, null, u, l), r.child = l; l; )
                l.flags = l.flags & -3 | 4096, l = l.sibling;
          else {
            if (wn(), u === c) {
              r = zn(n, r, l);
              break e;
            }
            jn(n, r, u, l);
          }
          r = r.child;
        }
        return r;
      case 5:
        return Zv(r), n === null && _c(r), u = r.type, c = r.pendingProps, d = n !== null ? n.memoizedProps : null, m = c.children, vs(u, c) ? m = null : d !== null && vs(u, d) && (r.flags |= 32), go(n, r), jn(n, r, m, l), r.child;
      case 6:
        return n === null && _c(r), null;
      case 13:
        return ch(n, r, l);
      case 4:
        return Ud(r, r.stateNode.containerInfo), u = r.pendingProps, n === null ? r.child = lu(r, null, u, l) : jn(n, r, u, l), r.child;
      case 11:
        return u = r.type, c = r.pendingProps, c = r.elementType === u ? c : ua(u, c), gu(n, r, u, c, l);
      case 7:
        return jn(n, r, r.pendingProps, l), r.child;
      case 8:
        return jn(n, r, r.pendingProps.children, l), r.child;
      case 12:
        return jn(n, r, r.pendingProps.children, l), r.child;
      case 10:
        e: {
          if (u = r.type._context, c = r.pendingProps, d = r.memoizedProps, m = c.value, Zt(qi, u._currentValue), u._currentValue = m, d !== null)
            if (Ua(d.value, m)) {
              if (d.children === c.children && !_n.current) {
                r = zn(n, r, l);
                break e;
              }
            } else
              for (d = r.child, d !== null && (d.return = r); d !== null; ) {
                var E = d.dependencies;
                if (E !== null) {
                  m = d.child;
                  for (var k = E.firstContext; k !== null; ) {
                    if (k.context === u) {
                      if (d.tag === 1) {
                        k = oa(-1, l & -l), k.tag = 2;
                        var H = d.updateQueue;
                        if (H !== null) {
                          H = H.shared;
                          var re = H.pending;
                          re === null ? k.next = k : (k.next = re.next, re.next = k), H.pending = k;
                        }
                      }
                      d.lanes |= l, k = d.alternate, k !== null && (k.lanes |= l), Ad(
                        d.return,
                        l,
                        r
                      ), E.lanes |= l;
                      break;
                    }
                    k = k.next;
                  }
                } else if (d.tag === 10)
                  m = d.type === r.type ? null : d.child;
                else if (d.tag === 18) {
                  if (m = d.return, m === null)
                    throw Error(b(341));
                  m.lanes |= l, E = m.alternate, E !== null && (E.lanes |= l), Ad(m, l, r), m = d.sibling;
                } else
                  m = d.child;
                if (m !== null)
                  m.return = d;
                else
                  for (m = d; m !== null; ) {
                    if (m === r) {
                      m = null;
                      break;
                    }
                    if (d = m.sibling, d !== null) {
                      d.return = m.return, m = d;
                      break;
                    }
                    m = m.return;
                  }
                d = m;
              }
          jn(n, r, c.children, l), r = r.child;
        }
        return r;
      case 9:
        return c = r.type, u = r.pendingProps.children, ou(r, l), c = Ia(c), u = u(c), r.flags |= 1, jn(n, r, u, l), r.child;
      case 14:
        return u = r.type, c = ua(u, r.pendingProps), c = ua(u.type, c), Al(n, r, u, c, l);
      case 15:
        return Zc(n, r, r.type, r.pendingProps, l);
      case 17:
        return u = r.type, c = r.pendingProps, c = r.elementType === u ? c : ua(u, c), Ns(n, r), r.tag = 1, yn(u) ? (n = !0, Rc(r)) : n = !1, ou(r, l), nh(r, u, c), Bd(r, u, c, l), ef(null, r, u, !0, n, l);
      case 19:
        return Wd(n, r, l);
      case 22:
        return ca(n, r, l);
    }
    throw Error(b(156, r.tag));
  };
  function Eh(n, r) {
    return ln(n, r);
  }
  function wh(n, r, l, u) {
    this.tag = n, this.key = l, this.sibling = this.child = this.return = this.stateNode = this.type = this.elementType = null, this.index = 0, this.ref = null, this.pendingProps = r, this.dependencies = this.memoizedState = this.updateQueue = this.memoizedProps = null, this.mode = u, this.subtreeFlags = this.flags = 0, this.deletions = null, this.childLanes = this.lanes = 0, this.alternate = null;
  }
  function Xa(n, r, l, u) {
    return new wh(n, r, l, u);
  }
  function rp(n) {
    return n = n.prototype, !(!n || !n.isReactComponent);
  }
  function Hy(n) {
    if (typeof n == "function")
      return rp(n) ? 1 : 0;
    if (n != null) {
      if (n = n.$$typeof, n === Rt)
        return 11;
      if (n === Nt)
        return 14;
    }
    return 2;
  }
  function Hl(n, r) {
    var l = n.alternate;
    return l === null ? (l = Xa(n.tag, r, n.key, n.mode), l.elementType = n.elementType, l.type = n.type, l.stateNode = n.stateNode, l.alternate = n, n.alternate = l) : (l.pendingProps = r, l.type = n.type, l.flags = 0, l.subtreeFlags = 0, l.deletions = null), l.flags = n.flags & 14680064, l.childLanes = n.childLanes, l.lanes = n.lanes, l.child = n.child, l.memoizedProps = n.memoizedProps, l.memoizedState = n.memoizedState, l.updateQueue = n.updateQueue, r = n.dependencies, l.dependencies = r === null ? null : { lanes: r.lanes, firstContext: r.firstContext }, l.sibling = n.sibling, l.index = n.index, l.ref = n.ref, l;
  }
  function yf(n, r, l, u, c, d) {
    var m = 2;
    if (u = n, typeof n == "function")
      rp(n) && (m = 1);
    else if (typeof n == "string")
      m = 5;
    else
      e:
        switch (n) {
          case Ye:
            return Ro(l.children, c, d, r);
          case be:
            m = 8, c |= 8;
            break;
          case Oe:
            return n = Xa(12, l, r, c | 2), n.elementType = Oe, n.lanes = d, n;
          case Ie:
            return n = Xa(13, l, r, c), n.elementType = Ie, n.lanes = d, n;
          case st:
            return n = Xa(19, l, r, c), n.elementType = st, n.lanes = d, n;
          case Se:
            return gf(l, c, d, r);
          default:
            if (typeof n == "object" && n !== null)
              switch (n.$$typeof) {
                case $e:
                  m = 10;
                  break e;
                case it:
                  m = 9;
                  break e;
                case Rt:
                  m = 11;
                  break e;
                case Nt:
                  m = 14;
                  break e;
                case yt:
                  m = 16, u = null;
                  break e;
              }
            throw Error(b(130, n == null ? n : typeof n, ""));
        }
    return r = Xa(m, l, r, c), r.elementType = n, r.type = u, r.lanes = d, r;
  }
  function Ro(n, r, l, u) {
    return n = Xa(7, n, u, r), n.lanes = l, n;
  }
  function gf(n, r, l, u) {
    return n = Xa(22, n, u, r), n.elementType = Se, n.lanes = l, n.stateNode = { isHidden: !1 }, n;
  }
  function Sf(n, r, l) {
    return n = Xa(6, n, null, r), n.lanes = l, n;
  }
  function As(n, r, l) {
    return r = Xa(4, n.children !== null ? n.children : [], n.key, r), r.lanes = l, r.stateNode = { containerInfo: n.containerInfo, pendingChildren: null, implementation: n.implementation }, r;
  }
  function Us(n, r, l, u, c) {
    this.tag = r, this.containerInfo = n, this.finishedWork = this.pingCache = this.current = this.pendingChildren = null, this.timeoutHandle = -1, this.callbackNode = this.pendingContext = this.context = null, this.callbackPriority = 0, this.eventTimes = Io(0), this.expirationTimes = Io(-1), this.entangledLanes = this.finishedLanes = this.mutableReadLanes = this.expiredLanes = this.pingedLanes = this.suspendedLanes = this.pendingLanes = 0, this.entanglements = Io(0), this.identifierPrefix = u, this.onRecoverableError = c, this.mutableSourceEagerHydrationData = null;
  }
  function ap(n, r, l, u, c, d, m, E, k) {
    return n = new Us(n, r, l, E, k), r === 1 ? (r = 1, d === !0 && (r |= 8)) : r = 0, d = Xa(3, null, null, r), n.current = d, d.stateNode = n, d.memoizedState = { element: u, isDehydrated: l, cache: null, transitions: null, pendingSuspenseBoundaries: null }, Mc(d), n;
  }
  function Rh(n, r, l) {
    var u = 3 < arguments.length && arguments[3] !== void 0 ? arguments[3] : null;
    return { $$typeof: at, key: u == null ? null : "" + u, children: n, containerInfo: r, implementation: l };
  }
  function ip(n) {
    if (!n)
      return wi;
    n = n._reactInternals;
    e: {
      if (Pe(n) !== n || n.tag !== 1)
        throw Error(b(170));
      var r = n;
      do {
        switch (r.tag) {
          case 3:
            r = r.stateNode.context;
            break e;
          case 1:
            if (yn(r.type)) {
              r = r.stateNode.__reactInternalMemoizedMergedChildContext;
              break e;
            }
        }
        r = r.return;
      } while (r !== null);
      throw Error(b(171));
    }
    if (n.tag === 1) {
      var l = n.type;
      if (yn(l))
        return ys(n, l, r);
    }
    return r;
  }
  function lp(n, r, l, u, c, d, m, E, k) {
    return n = ap(l, u, !0, n, c, d, m, E, k), n.context = ip(null), l = n.current, u = or(), c = el(l), d = oa(u, c), d.callback = r ?? null, Ll(l, d, c), n.current.lanes = c, Fi(n, c, u), Xn(n, u), n;
  }
  function xf(n, r, l, u) {
    var c = r.current, d = or(), m = el(c);
    return l = ip(l), r.context === null ? r.context = l : r.pendingContext = l, r = oa(d, m), r.payload = { element: n }, u = u === void 0 ? null : u, u !== null && (r.callback = u), n = Ll(c, r, m), n !== null && (Rn(n, c, m, d), Lc(n, c, m)), m;
  }
  function Fs(n) {
    if (n = n.current, !n.child)
      return null;
    switch (n.child.tag) {
      case 5:
        return n.child.stateNode;
      default:
        return n.child.stateNode;
    }
  }
  function Th(n, r) {
    if (n = n.memoizedState, n !== null && n.dehydrated !== null) {
      var l = n.retryLane;
      n.retryLane = l !== 0 && l < r ? l : r;
    }
  }
  function op(n, r) {
    Th(n, r), (n = n.alternate) && Th(n, r);
  }
  function Py() {
    return null;
  }
  var up = typeof reportError == "function" ? reportError : function(n) {
    console.error(n);
  };
  function bf(n) {
    this._internalRoot = n;
  }
  Hs.prototype.render = bf.prototype.render = function(n) {
    var r = this._internalRoot;
    if (r === null)
      throw Error(b(409));
    xf(n, r, null, null);
  }, Hs.prototype.unmount = bf.prototype.unmount = function() {
    var n = this._internalRoot;
    if (n !== null) {
      this._internalRoot = null;
      var r = n.containerInfo;
      Di(function() {
        xf(null, n, null, null);
      }), r[Qi] = null;
    }
  };
  function Hs(n) {
    this._internalRoot = n;
  }
  Hs.prototype.unstable_scheduleHydration = function(n) {
    if (n) {
      var r = Qo();
      n = { blockedOn: null, target: n, priority: r };
      for (var l = 0; l < Jt.length && r !== 0 && r < Jt[l].priority; l++)
        ;
      Jt.splice(l, 0, n), l === 0 && dc(n);
    }
  };
  function Pl(n) {
    return !(!n || n.nodeType !== 1 && n.nodeType !== 9 && n.nodeType !== 11);
  }
  function Cf(n) {
    return !(!n || n.nodeType !== 1 && n.nodeType !== 9 && n.nodeType !== 11 && (n.nodeType !== 8 || n.nodeValue !== " react-mount-point-unstable "));
  }
  function kh() {
  }
  function Vy(n, r, l, u, c) {
    if (c) {
      if (typeof u == "function") {
        var d = u;
        u = function() {
          var H = Fs(m);
          d.call(H);
        };
      }
      var m = lp(r, u, n, 0, null, !1, !1, "", kh);
      return n._reactRootContainer = m, n[Qi] = m.current, ru(n.nodeType === 8 ? n.parentNode : n), Di(), m;
    }
    for (; c = n.lastChild; )
      n.removeChild(c);
    if (typeof u == "function") {
      var E = u;
      u = function() {
        var H = Fs(k);
        E.call(H);
      };
    }
    var k = ap(n, 0, !1, null, null, !1, !1, "", kh);
    return n._reactRootContainer = k, n[Qi] = k.current, ru(n.nodeType === 8 ? n.parentNode : n), Di(function() {
      xf(r, k, l, u);
    }), k;
  }
  function Ef(n, r, l, u, c) {
    var d = l._reactRootContainer;
    if (d) {
      var m = d;
      if (typeof c == "function") {
        var E = c;
        c = function() {
          var k = Fs(m);
          E.call(k);
        };
      }
      xf(r, m, n, c);
    } else
      m = Vy(l, r, n, c, u);
    return Fs(m);
  }
  Jl = function(n) {
    switch (n.tag) {
      case 3:
        var r = n.stateNode;
        if (r.current.memoizedState.isDehydrated) {
          var l = li(r.pendingLanes);
          l !== 0 && (bi(r, l | 1), Xn(r, Vt()), !(Ot & 6) && (Nu = Vt() + 500, ra()));
        }
        break;
      case 13:
        Di(function() {
          var u = Xi(n, 1);
          if (u !== null) {
            var c = or();
            Rn(u, n, 1, c);
          }
        }), op(n, 1);
    }
  }, Wo = function(n) {
    if (n.tag === 13) {
      var r = Xi(n, 134217728);
      if (r !== null) {
        var l = or();
        Rn(r, n, 134217728, l);
      }
      op(n, 134217728);
    }
  }, zt = function(n) {
    if (n.tag === 13) {
      var r = el(n), l = Xi(n, r);
      if (l !== null) {
        var u = or();
        Rn(l, n, r, u);
      }
      op(n, r);
    }
  }, Qo = function() {
    return Bt;
  }, Go = function(n, r) {
    var l = Bt;
    try {
      return Bt = n, r();
    } finally {
      Bt = l;
    }
  }, Mr = function(n, r, l) {
    switch (r) {
      case "input":
        if (Mn(n, l), r = l.name, l.type === "radio" && r != null) {
          for (l = n; l.parentNode; )
            l = l.parentNode;
          for (l = l.querySelectorAll("input[name=" + JSON.stringify("" + r) + '][type="radio"]'), r = 0; r < l.length; r++) {
            var u = l[r];
            if (u !== n && u.form === n.form) {
              var c = qe(u);
              if (!c)
                throw Error(b(90));
              Yn(u), Mn(u, c);
            }
          }
        }
        break;
      case "textarea":
        ya(n, l);
        break;
      case "select":
        r = l.value, r != null && Cr(n, !!l.multiple, r, !1);
    }
  }, Kl = tp, Po = Di;
  var By = { usingClientEntryPoint: !1, Events: [ms, au, qe, La, pl, tp] }, Ps = { findFiberByHostInstance: Fa, bundleType: 0, version: "18.3.1", rendererPackageName: "react-dom" }, _h = { bundleType: Ps.bundleType, version: Ps.version, rendererPackageName: Ps.rendererPackageName, rendererConfig: Ps.rendererConfig, overrideHookState: null, overrideHookStateDeletePath: null, overrideHookStateRenamePath: null, overrideProps: null, overridePropsDeletePath: null, overridePropsRenamePath: null, setErrorHandler: null, setSuspenseHandler: null, scheduleUpdate: null, currentDispatcherRef: ct.ReactCurrentDispatcher, findHostInstanceByFiber: function(n) {
    return n = Ct(n), n === null ? null : n.stateNode;
  }, findFiberByHostInstance: Ps.findFiberByHostInstance || Py, findHostInstancesForRefresh: null, scheduleRefresh: null, scheduleRoot: null, setRefreshHandler: null, getCurrentFiber: null, reconcilerVersion: "18.3.1-next-f1338f8080-20240426" };
  if (typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ < "u") {
    var wf = __REACT_DEVTOOLS_GLOBAL_HOOK__;
    if (!wf.isDisabled && wf.supportsFiber)
      try {
        ml = wf.inject(_h), Jr = wf;
      } catch {
      }
  }
  return ni.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED = By, ni.createPortal = function(n, r) {
    var l = 2 < arguments.length && arguments[2] !== void 0 ? arguments[2] : null;
    if (!Pl(r))
      throw Error(b(200));
    return Rh(n, r, null, l);
  }, ni.createRoot = function(n, r) {
    if (!Pl(n))
      throw Error(b(299));
    var l = !1, u = "", c = up;
    return r != null && (r.unstable_strictMode === !0 && (l = !0), r.identifierPrefix !== void 0 && (u = r.identifierPrefix), r.onRecoverableError !== void 0 && (c = r.onRecoverableError)), r = ap(n, 1, !1, null, null, l, !1, u, c), n[Qi] = r.current, ru(n.nodeType === 8 ? n.parentNode : n), new bf(r);
  }, ni.findDOMNode = function(n) {
    if (n == null)
      return null;
    if (n.nodeType === 1)
      return n;
    var r = n._reactInternals;
    if (r === void 0)
      throw typeof n.render == "function" ? Error(b(188)) : (n = Object.keys(n).join(","), Error(b(268, n)));
    return n = Ct(r), n = n === null ? null : n.stateNode, n;
  }, ni.flushSync = function(n) {
    return Di(n);
  }, ni.hydrate = function(n, r, l) {
    if (!Cf(r))
      throw Error(b(200));
    return Ef(null, n, r, !0, l);
  }, ni.hydrateRoot = function(n, r, l) {
    if (!Pl(n))
      throw Error(b(405));
    var u = l != null && l.hydratedSources || null, c = !1, d = "", m = up;
    if (l != null && (l.unstable_strictMode === !0 && (c = !0), l.identifierPrefix !== void 0 && (d = l.identifierPrefix), l.onRecoverableError !== void 0 && (m = l.onRecoverableError)), r = lp(r, null, n, 1, l ?? null, c, !1, d, m), n[Qi] = r.current, ru(n), u)
      for (n = 0; n < u.length; n++)
        l = u[n], c = l._getVersion, c = c(l._source), r.mutableSourceEagerHydrationData == null ? r.mutableSourceEagerHydrationData = [l, c] : r.mutableSourceEagerHydrationData.push(
          l,
          c
        );
    return new Hs(r);
  }, ni.render = function(n, r, l) {
    if (!Cf(r))
      throw Error(b(200));
    return Ef(null, n, r, !1, l);
  }, ni.unmountComponentAtNode = function(n) {
    if (!Cf(n))
      throw Error(b(40));
    return n._reactRootContainer ? (Di(function() {
      Ef(null, null, n, !1, function() {
        n._reactRootContainer = null, n[Qi] = null;
      });
    }), !0) : !1;
  }, ni.unstable_batchedUpdates = tp, ni.unstable_renderSubtreeIntoContainer = function(n, r, l, u) {
    if (!Cf(l))
      throw Error(b(200));
    if (n == null || n._reactInternals === void 0)
      throw Error(b(38));
    return Ef(n, r, l, !1, u);
  }, ni.version = "18.3.1-next-f1338f8080-20240426", ni;
}
var ri = {};
/**
 * @license React
 * react-dom.development.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var LE;
function eD() {
  return LE || (LE = 1, process.env.NODE_ENV !== "production" && function() {
    typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ < "u" && typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.registerInternalModuleStart == "function" && __REACT_DEVTOOLS_GLOBAL_HOOK__.registerInternalModuleStart(new Error());
    var S = wt, w = PE(), b = S.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED, U = !1;
    function X(e) {
      U = e;
    }
    function W(e) {
      if (!U) {
        for (var t = arguments.length, a = new Array(t > 1 ? t - 1 : 0), i = 1; i < t; i++)
          a[i - 1] = arguments[i];
        ce("warn", e, a);
      }
    }
    function y(e) {
      if (!U) {
        for (var t = arguments.length, a = new Array(t > 1 ? t - 1 : 0), i = 1; i < t; i++)
          a[i - 1] = arguments[i];
        ce("error", e, a);
      }
    }
    function ce(e, t, a) {
      {
        var i = b.ReactDebugCurrentFrame, o = i.getStackAddendum();
        o !== "" && (t += "%s", a = a.concat([o]));
        var s = a.map(function(f) {
          return String(f);
        });
        s.unshift("Warning: " + t), Function.prototype.apply.call(console[e], console, s);
      }
    }
    var B = 0, K = 1, ye = 2, ne = 3, oe = 4, V = 5, $ = 6, de = 7, Ae = 8, Dt = 9, rt = 10, Ke = 11, ct = 12, ke = 13, at = 14, Ye = 15, be = 16, Oe = 17, $e = 18, it = 19, Rt = 21, Ie = 22, st = 23, Nt = 24, yt = 25, Se = !0, I = !1, Ue = !1, pe = !1, O = !1, q = !0, Re = !1, Me = !0, ft = !0, vt = !0, Ge = !0, St = /* @__PURE__ */ new Set(), ht = {}, Wt = {};
    function Fn(e, t) {
      Yn(e, t), Yn(e + "Capture", t);
    }
    function Yn(e, t) {
      ht[e] && y("EventRegistry: More than one plugin attempted to publish the same registration name, `%s`.", e), ht[e] = t;
      {
        var a = e.toLowerCase();
        Wt[a] = e, e === "onDoubleClick" && (Wt.ondblclick = e);
      }
      for (var i = 0; i < t.length; i++)
        St.add(t[i]);
    }
    var xn = typeof window < "u" && typeof window.document < "u" && typeof window.document.createElement < "u", Zn = Object.prototype.hasOwnProperty;
    function Wn(e) {
      {
        var t = typeof Symbol == "function" && Symbol.toStringTag, a = t && e[Symbol.toStringTag] || e.constructor.name || "Object";
        return a;
      }
    }
    function Hn(e) {
      try {
        return Mn(e), !1;
      } catch {
        return !0;
      }
    }
    function Mn(e) {
      return "" + e;
    }
    function Gr(e, t) {
      if (Hn(e))
        return y("The provided `%s` attribute is an unsupported type %s. This value must be coerced to a string before before using it here.", t, Wn(e)), Mn(e);
    }
    function qr(e) {
      if (Hn(e))
        return y("The provided key is an unsupported type %s. This value must be coerced to a string before before using it here.", Wn(e)), Mn(e);
    }
    function er(e, t) {
      if (Hn(e))
        return y("The provided `%s` prop is an unsupported type %s. This value must be coerced to a string before before using it here.", t, Wn(e)), Mn(e);
    }
    function Cr(e, t) {
      if (Hn(e))
        return y("The provided `%s` CSS property is an unsupported type %s. This value must be coerced to a string before before using it here.", t, Wn(e)), Mn(e);
    }
    function Xr(e) {
      if (Hn(e))
        return y("The provided HTML markup uses a value of unsupported type %s. This value must be coerced to a string before before using it here.", Wn(e)), Mn(e);
    }
    function Er(e) {
      if (Hn(e))
        return y("Form field values (value, checked, defaultValue, or defaultChecked props) must be strings, not %s. This value must be coerced to a string before before using it here.", Wn(e)), Mn(e);
    }
    var ya = 0, sr = 1, Kr = 2, bn = 3, Or = 4, mi = 5, ga = 6, fe = ":A-Z_a-z\\u00C0-\\u00D6\\u00D8-\\u00F6\\u00F8-\\u02FF\\u0370-\\u037D\\u037F-\\u1FFF\\u200C-\\u200D\\u2070-\\u218F\\u2C00-\\u2FEF\\u3001-\\uD7FF\\uF900-\\uFDCF\\uFDF0-\\uFFFD", We = fe + "\\-.0-9\\u00B7\\u0300-\\u036F\\u203F-\\u2040", bt = new RegExp("^[" + fe + "][" + We + "]*$"), Qt = {}, qt = {};
    function Ln(e) {
      return Zn.call(qt, e) ? !0 : Zn.call(Qt, e) ? !1 : bt.test(e) ? (qt[e] = !0, !0) : (Qt[e] = !0, y("Invalid attribute name: `%s`", e), !1);
    }
    function Cn(e, t, a) {
      return t !== null ? t.type === ya : a ? !1 : e.length > 2 && (e[0] === "o" || e[0] === "O") && (e[1] === "n" || e[1] === "N");
    }
    function wr(e, t, a, i) {
      if (a !== null && a.type === ya)
        return !1;
      switch (typeof t) {
        case "function":
        case "symbol":
          return !0;
        case "boolean": {
          if (i)
            return !1;
          if (a !== null)
            return !a.acceptsBooleans;
          var o = e.toLowerCase().slice(0, 5);
          return o !== "data-" && o !== "aria-";
        }
        default:
          return !1;
      }
    }
    function tn(e, t, a, i) {
      if (t === null || typeof t > "u" || wr(e, t, a, i))
        return !0;
      if (i)
        return !1;
      if (a !== null)
        switch (a.type) {
          case bn:
            return !t;
          case Or:
            return t === !1;
          case mi:
            return isNaN(t);
          case ga:
            return isNaN(t) || t < 1;
        }
      return !1;
    }
    function Mr(e) {
      return Kt.hasOwnProperty(e) ? Kt[e] : null;
    }
    function Xt(e, t, a, i, o, s, f) {
      this.acceptsBooleans = t === Kr || t === bn || t === Or, this.attributeName = i, this.attributeNamespace = o, this.mustUseProperty = a, this.propertyName = e, this.type = t, this.sanitizeURL = s, this.removeEmptyString = f;
    }
    var Kt = {}, ai = [
      "children",
      "dangerouslySetInnerHTML",
      // TODO: This prevents the assignment of defaultValue to regular
      // elements (not just inputs). Now that ReactDOMInput assigns to the
      // defaultValue property -- do we need this?
      "defaultValue",
      "defaultChecked",
      "innerHTML",
      "suppressContentEditableWarning",
      "suppressHydrationWarning",
      "style"
    ];
    ai.forEach(function(e) {
      Kt[e] = new Xt(
        e,
        ya,
        !1,
        // mustUseProperty
        e,
        // attributeName
        null,
        // attributeNamespace
        !1,
        // sanitizeURL
        !1
      );
    }), [["acceptCharset", "accept-charset"], ["className", "class"], ["htmlFor", "for"], ["httpEquiv", "http-equiv"]].forEach(function(e) {
      var t = e[0], a = e[1];
      Kt[t] = new Xt(
        t,
        sr,
        !1,
        // mustUseProperty
        a,
        // attributeName
        null,
        // attributeNamespace
        !1,
        // sanitizeURL
        !1
      );
    }), ["contentEditable", "draggable", "spellCheck", "value"].forEach(function(e) {
      Kt[e] = new Xt(
        e,
        Kr,
        !1,
        // mustUseProperty
        e.toLowerCase(),
        // attributeName
        null,
        // attributeNamespace
        !1,
        // sanitizeURL
        !1
      );
    }), ["autoReverse", "externalResourcesRequired", "focusable", "preserveAlpha"].forEach(function(e) {
      Kt[e] = new Xt(
        e,
        Kr,
        !1,
        // mustUseProperty
        e,
        // attributeName
        null,
        // attributeNamespace
        !1,
        // sanitizeURL
        !1
      );
    }), [
      "allowFullScreen",
      "async",
      // Note: there is a special case that prevents it from being written to the DOM
      // on the client side because the browsers are inconsistent. Instead we call focus().
      "autoFocus",
      "autoPlay",
      "controls",
      "default",
      "defer",
      "disabled",
      "disablePictureInPicture",
      "disableRemotePlayback",
      "formNoValidate",
      "hidden",
      "loop",
      "noModule",
      "noValidate",
      "open",
      "playsInline",
      "readOnly",
      "required",
      "reversed",
      "scoped",
      "seamless",
      // Microdata
      "itemScope"
    ].forEach(function(e) {
      Kt[e] = new Xt(
        e,
        bn,
        !1,
        // mustUseProperty
        e.toLowerCase(),
        // attributeName
        null,
        // attributeNamespace
        !1,
        // sanitizeURL
        !1
      );
    }), [
      "checked",
      // Note: `option.selected` is not updated if `select.multiple` is
      // disabled with `removeAttribute`. We have special logic for handling this.
      "multiple",
      "muted",
      "selected"
      // NOTE: if you add a camelCased prop to this list,
      // you'll need to set attributeName to name.toLowerCase()
      // instead in the assignment below.
    ].forEach(function(e) {
      Kt[e] = new Xt(
        e,
        bn,
        !0,
        // mustUseProperty
        e,
        // attributeName
        null,
        // attributeNamespace
        !1,
        // sanitizeURL
        !1
      );
    }), [
      "capture",
      "download"
      // NOTE: if you add a camelCased prop to this list,
      // you'll need to set attributeName to name.toLowerCase()
      // instead in the assignment below.
    ].forEach(function(e) {
      Kt[e] = new Xt(
        e,
        Or,
        !1,
        // mustUseProperty
        e,
        // attributeName
        null,
        // attributeNamespace
        !1,
        // sanitizeURL
        !1
      );
    }), [
      "cols",
      "rows",
      "size",
      "span"
      // NOTE: if you add a camelCased prop to this list,
      // you'll need to set attributeName to name.toLowerCase()
      // instead in the assignment below.
    ].forEach(function(e) {
      Kt[e] = new Xt(
        e,
        ga,
        !1,
        // mustUseProperty
        e,
        // attributeName
        null,
        // attributeNamespace
        !1,
        // sanitizeURL
        !1
      );
    }), ["rowSpan", "start"].forEach(function(e) {
      Kt[e] = new Xt(
        e,
        mi,
        !1,
        // mustUseProperty
        e.toLowerCase(),
        // attributeName
        null,
        // attributeNamespace
        !1,
        // sanitizeURL
        !1
      );
    });
    var La = /[\-\:]([a-z])/g, pl = function(e) {
      return e[1].toUpperCase();
    };
    [
      "accent-height",
      "alignment-baseline",
      "arabic-form",
      "baseline-shift",
      "cap-height",
      "clip-path",
      "clip-rule",
      "color-interpolation",
      "color-interpolation-filters",
      "color-profile",
      "color-rendering",
      "dominant-baseline",
      "enable-background",
      "fill-opacity",
      "fill-rule",
      "flood-color",
      "flood-opacity",
      "font-family",
      "font-size",
      "font-size-adjust",
      "font-stretch",
      "font-style",
      "font-variant",
      "font-weight",
      "glyph-name",
      "glyph-orientation-horizontal",
      "glyph-orientation-vertical",
      "horiz-adv-x",
      "horiz-origin-x",
      "image-rendering",
      "letter-spacing",
      "lighting-color",
      "marker-end",
      "marker-mid",
      "marker-start",
      "overline-position",
      "overline-thickness",
      "paint-order",
      "panose-1",
      "pointer-events",
      "rendering-intent",
      "shape-rendering",
      "stop-color",
      "stop-opacity",
      "strikethrough-position",
      "strikethrough-thickness",
      "stroke-dasharray",
      "stroke-dashoffset",
      "stroke-linecap",
      "stroke-linejoin",
      "stroke-miterlimit",
      "stroke-opacity",
      "stroke-width",
      "text-anchor",
      "text-decoration",
      "text-rendering",
      "underline-position",
      "underline-thickness",
      "unicode-bidi",
      "unicode-range",
      "units-per-em",
      "v-alphabetic",
      "v-hanging",
      "v-ideographic",
      "v-mathematical",
      "vector-effect",
      "vert-adv-y",
      "vert-origin-x",
      "vert-origin-y",
      "word-spacing",
      "writing-mode",
      "xmlns:xlink",
      "x-height"
      // NOTE: if you add a camelCased prop to this list,
      // you'll need to set attributeName to name.toLowerCase()
      // instead in the assignment below.
    ].forEach(function(e) {
      var t = e.replace(La, pl);
      Kt[t] = new Xt(
        t,
        sr,
        !1,
        // mustUseProperty
        e,
        null,
        // attributeNamespace
        !1,
        // sanitizeURL
        !1
      );
    }), [
      "xlink:actuate",
      "xlink:arcrole",
      "xlink:role",
      "xlink:show",
      "xlink:title",
      "xlink:type"
      // NOTE: if you add a camelCased prop to this list,
      // you'll need to set attributeName to name.toLowerCase()
      // instead in the assignment below.
    ].forEach(function(e) {
      var t = e.replace(La, pl);
      Kt[t] = new Xt(
        t,
        sr,
        !1,
        // mustUseProperty
        e,
        "http://www.w3.org/1999/xlink",
        !1,
        // sanitizeURL
        !1
      );
    }), [
      "xml:base",
      "xml:lang",
      "xml:space"
      // NOTE: if you add a camelCased prop to this list,
      // you'll need to set attributeName to name.toLowerCase()
      // instead in the assignment below.
    ].forEach(function(e) {
      var t = e.replace(La, pl);
      Kt[t] = new Xt(
        t,
        sr,
        !1,
        // mustUseProperty
        e,
        "http://www.w3.org/XML/1998/namespace",
        !1,
        // sanitizeURL
        !1
      );
    }), ["tabIndex", "crossOrigin"].forEach(function(e) {
      Kt[e] = new Xt(
        e,
        sr,
        !1,
        // mustUseProperty
        e.toLowerCase(),
        // attributeName
        null,
        // attributeNamespace
        !1,
        // sanitizeURL
        !1
      );
    });
    var Kl = "xlinkHref";
    Kt[Kl] = new Xt(
      "xlinkHref",
      sr,
      !1,
      // mustUseProperty
      "xlink:href",
      "http://www.w3.org/1999/xlink",
      !0,
      // sanitizeURL
      !1
    ), ["src", "href", "action", "formAction"].forEach(function(e) {
      Kt[e] = new Xt(
        e,
        sr,
        !1,
        // mustUseProperty
        e.toLowerCase(),
        // attributeName
        null,
        // attributeNamespace
        !0,
        // sanitizeURL
        !0
      );
    });
    var Po = /^[\u0000-\u001F ]*j[\r\n\t]*a[\r\n\t]*v[\r\n\t]*a[\r\n\t]*s[\r\n\t]*c[\r\n\t]*r[\r\n\t]*i[\r\n\t]*p[\r\n\t]*t[\r\n\t]*\:/i, Ui = !1;
    function vl(e) {
      !Ui && Po.test(e) && (Ui = !0, y("A future version of React will block javascript: URLs as a security precaution. Use event handlers instead if you can. If you need to generate unsafe HTML try using dangerouslySetInnerHTML instead. React was passed %s.", JSON.stringify(e)));
    }
    function Sa(e, t, a, i) {
      if (i.mustUseProperty) {
        var o = i.propertyName;
        return e[o];
      } else {
        Gr(a, t), i.sanitizeURL && vl("" + a);
        var s = i.attributeName, f = null;
        if (i.type === Or) {
          if (e.hasAttribute(s)) {
            var p = e.getAttribute(s);
            return p === "" ? !0 : tn(t, a, i, !1) ? p : p === "" + a ? a : p;
          }
        } else if (e.hasAttribute(s)) {
          if (tn(t, a, i, !1))
            return e.getAttribute(s);
          if (i.type === bn)
            return a;
          f = e.getAttribute(s);
        }
        return tn(t, a, i, !1) ? f === null ? a : f : f === "" + a ? a : f;
      }
    }
    function yi(e, t, a, i) {
      {
        if (!Ln(t))
          return;
        if (!e.hasAttribute(t))
          return a === void 0 ? void 0 : null;
        var o = e.getAttribute(t);
        return Gr(a, t), o === "" + a ? a : o;
      }
    }
    function xa(e, t, a, i) {
      var o = Mr(t);
      if (!Cn(t, o, i)) {
        if (tn(t, a, o, i) && (a = null), i || o === null) {
          if (Ln(t)) {
            var s = t;
            a === null ? e.removeAttribute(s) : (Gr(a, t), e.setAttribute(s, "" + a));
          }
          return;
        }
        var f = o.mustUseProperty;
        if (f) {
          var p = o.propertyName;
          if (a === null) {
            var v = o.type;
            e[p] = v === bn ? !1 : "";
          } else
            e[p] = a;
          return;
        }
        var g = o.attributeName, x = o.attributeNamespace;
        if (a === null)
          e.removeAttribute(g);
        else {
          var N = o.type, _;
          N === bn || N === Or && a === !0 ? _ = "" : (Gr(a, g), _ = "" + a, o.sanitizeURL && vl(_.toString())), x ? e.setAttributeNS(x, g, _) : e.setAttribute(g, _);
        }
      }
    }
    var ii = Symbol.for("react.element"), Lr = Symbol.for("react.portal"), ba = Symbol.for("react.fragment"), gi = Symbol.for("react.strict_mode"), Si = Symbol.for("react.profiler"), T = Symbol.for("react.provider"), ee = Symbol.for("react.context"), ie = Symbol.for("react.forward_ref"), Pe = Symbol.for("react.suspense"), Tt = Symbol.for("react.suspense_list"), jt = Symbol.for("react.memo"), Ze = Symbol.for("react.lazy"), Ct = Symbol.for("react.scope"), Pn = Symbol.for("react.debug_trace_mode"), ln = Symbol.for("react.offscreen"), dn = Symbol.for("react.legacy_hidden"), Rr = Symbol.for("react.cache"), xi = Symbol.for("react.tracing_marker"), Vt = Symbol.iterator, tr = "@@iterator";
    function jr(e) {
      if (e === null || typeof e != "object")
        return null;
      var t = Vt && e[Vt] || e[tr];
      return typeof t == "function" ? t : null;
    }
    var Et = Object.assign, ja = 0, hl, Vo, ml, Jr, Zu, zr, es;
    function ts() {
    }
    ts.__reactDisabledLog = !0;
    function cc() {
      {
        if (ja === 0) {
          hl = console.log, Vo = console.info, ml = console.warn, Jr = console.error, Zu = console.group, zr = console.groupCollapsed, es = console.groupEnd;
          var e = {
            configurable: !0,
            enumerable: !0,
            value: ts,
            writable: !0
          };
          Object.defineProperties(console, {
            info: e,
            log: e,
            warn: e,
            error: e,
            group: e,
            groupCollapsed: e,
            groupEnd: e
          });
        }
        ja++;
      }
    }
    function Bo() {
      {
        if (ja--, ja === 0) {
          var e = {
            configurable: !0,
            enumerable: !0,
            writable: !0
          };
          Object.defineProperties(console, {
            log: Et({}, e, {
              value: hl
            }),
            info: Et({}, e, {
              value: Vo
            }),
            warn: Et({}, e, {
              value: ml
            }),
            error: Et({}, e, {
              value: Jr
            }),
            group: Et({}, e, {
              value: Zu
            }),
            groupCollapsed: Et({}, e, {
              value: zr
            }),
            groupEnd: Et({}, e, {
              value: es
            })
          });
        }
        ja < 0 && y("disabledDepth fell below zero. This is a bug in React. Please file an issue.");
      }
    }
    var yl = b.ReactCurrentDispatcher, li;
    function Ar(e, t, a) {
      {
        if (li === void 0)
          try {
            throw Error();
          } catch (o) {
            var i = o.stack.trim().match(/\n( *(at )?)/);
            li = i && i[1] || "";
          }
        return `
` + li + e;
      }
    }
    var gl = !1, Sl;
    {
      var xl = typeof WeakMap == "function" ? WeakMap : Map;
      Sl = new xl();
    }
    function $o(e, t) {
      if (!e || gl)
        return "";
      {
        var a = Sl.get(e);
        if (a !== void 0)
          return a;
      }
      var i;
      gl = !0;
      var o = Error.prepareStackTrace;
      Error.prepareStackTrace = void 0;
      var s;
      s = yl.current, yl.current = null, cc();
      try {
        if (t) {
          var f = function() {
            throw Error();
          };
          if (Object.defineProperty(f.prototype, "props", {
            set: function() {
              throw Error();
            }
          }), typeof Reflect == "object" && Reflect.construct) {
            try {
              Reflect.construct(f, []);
            } catch (P) {
              i = P;
            }
            Reflect.construct(e, [], f);
          } else {
            try {
              f.call();
            } catch (P) {
              i = P;
            }
            e.call(f.prototype);
          }
        } else {
          try {
            throw Error();
          } catch (P) {
            i = P;
          }
          e();
        }
      } catch (P) {
        if (P && i && typeof P.stack == "string") {
          for (var p = P.stack.split(`
`), v = i.stack.split(`
`), g = p.length - 1, x = v.length - 1; g >= 1 && x >= 0 && p[g] !== v[x]; )
            x--;
          for (; g >= 1 && x >= 0; g--, x--)
            if (p[g] !== v[x]) {
              if (g !== 1 || x !== 1)
                do
                  if (g--, x--, x < 0 || p[g] !== v[x]) {
                    var N = `
` + p[g].replace(" at new ", " at ");
                    return e.displayName && N.includes("<anonymous>") && (N = N.replace("<anonymous>", e.displayName)), typeof e == "function" && Sl.set(e, N), N;
                  }
                while (g >= 1 && x >= 0);
              break;
            }
        }
      } finally {
        gl = !1, yl.current = s, Bo(), Error.prepareStackTrace = o;
      }
      var _ = e ? e.displayName || e.name : "", A = _ ? Ar(_) : "";
      return typeof e == "function" && Sl.set(e, A), A;
    }
    function Io(e, t, a) {
      return $o(e, !0);
    }
    function Fi(e, t, a) {
      return $o(e, !1);
    }
    function id(e) {
      var t = e.prototype;
      return !!(t && t.isReactComponent);
    }
    function bi(e, t, a) {
      if (e == null)
        return "";
      if (typeof e == "function")
        return $o(e, id(e));
      if (typeof e == "string")
        return Ar(e);
      switch (e) {
        case Pe:
          return Ar("Suspense");
        case Tt:
          return Ar("SuspenseList");
      }
      if (typeof e == "object")
        switch (e.$$typeof) {
          case ie:
            return Fi(e.render);
          case jt:
            return bi(e.type, t, a);
          case Ze: {
            var i = e, o = i._payload, s = i._init;
            try {
              return bi(s(o), t, a);
            } catch {
            }
          }
        }
      return "";
    }
    function Bt(e) {
      switch (e._debugOwner && e._debugOwner.type, e._debugSource, e.tag) {
        case V:
          return Ar(e.type);
        case be:
          return Ar("Lazy");
        case ke:
          return Ar("Suspense");
        case it:
          return Ar("SuspenseList");
        case B:
        case ye:
        case Ye:
          return Fi(e.type);
        case Ke:
          return Fi(e.type.render);
        case K:
          return Io(e.type);
        default:
          return "";
      }
    }
    function Yo(e) {
      try {
        var t = "", a = e;
        do
          t += Bt(a), a = a.return;
        while (a);
        return t;
      } catch (i) {
        return `
Error generating stack: ` + i.message + `
` + i.stack;
      }
    }
    function Jl(e, t, a) {
      var i = e.displayName;
      if (i)
        return i;
      var o = t.displayName || t.name || "";
      return o !== "" ? a + "(" + o + ")" : a;
    }
    function Wo(e) {
      return e.displayName || "Context";
    }
    function zt(e) {
      if (e == null)
        return null;
      if (typeof e.tag == "number" && y("Received an unexpected object in getComponentNameFromType(). This is likely a bug in React. Please file an issue."), typeof e == "function")
        return e.displayName || e.name || null;
      if (typeof e == "string")
        return e;
      switch (e) {
        case ba:
          return "Fragment";
        case Lr:
          return "Portal";
        case Si:
          return "Profiler";
        case gi:
          return "StrictMode";
        case Pe:
          return "Suspense";
        case Tt:
          return "SuspenseList";
      }
      if (typeof e == "object")
        switch (e.$$typeof) {
          case ee:
            var t = e;
            return Wo(t) + ".Consumer";
          case T:
            var a = e;
            return Wo(a._context) + ".Provider";
          case ie:
            return Jl(e, e.render, "ForwardRef");
          case jt:
            var i = e.displayName || null;
            return i !== null ? i : zt(e.type) || "Memo";
          case Ze: {
            var o = e, s = o._payload, f = o._init;
            try {
              return zt(f(s));
            } catch {
              return null;
            }
          }
        }
      return null;
    }
    function Qo(e, t, a) {
      var i = t.displayName || t.name || "";
      return e.displayName || (i !== "" ? a + "(" + i + ")" : a);
    }
    function Go(e) {
      return e.displayName || "Context";
    }
    function dt(e) {
      var t = e.tag, a = e.type;
      switch (t) {
        case Nt:
          return "Cache";
        case Dt:
          var i = a;
          return Go(i) + ".Consumer";
        case rt:
          var o = a;
          return Go(o._context) + ".Provider";
        case $e:
          return "DehydratedFragment";
        case Ke:
          return Qo(a, a.render, "ForwardRef");
        case de:
          return "Fragment";
        case V:
          return a;
        case oe:
          return "Portal";
        case ne:
          return "Root";
        case $:
          return "Text";
        case be:
          return zt(a);
        case Ae:
          return a === gi ? "StrictMode" : "Mode";
        case Ie:
          return "Offscreen";
        case ct:
          return "Profiler";
        case Rt:
          return "Scope";
        case ke:
          return "Suspense";
        case it:
          return "SuspenseList";
        case yt:
          return "TracingMarker";
        case K:
        case B:
        case Oe:
        case ye:
        case at:
        case Ye:
          if (typeof a == "function")
            return a.displayName || a.name || null;
          if (typeof a == "string")
            return a;
          break;
      }
      return null;
    }
    var Zl = b.ReactDebugCurrentFrame, En = null, Zr = !1;
    function Ur() {
      {
        if (En === null)
          return null;
        var e = En._debugOwner;
        if (e !== null && typeof e < "u")
          return dt(e);
      }
      return null;
    }
    function bl() {
      return En === null ? "" : Yo(En);
    }
    function kn() {
      Zl.getCurrentStack = null, En = null, Zr = !1;
    }
    function Jt(e) {
      Zl.getCurrentStack = e === null ? null : bl, En = e, Zr = !1;
    }
    function fc() {
      return En;
    }
    function ea(e) {
      Zr = e;
    }
    function nr(e) {
      return "" + e;
    }
    function Ci(e) {
      switch (typeof e) {
        case "boolean":
        case "number":
        case "string":
        case "undefined":
          return e;
        case "object":
          return Er(e), e;
        default:
          return "";
      }
    }
    var dc = {
      button: !0,
      checkbox: !0,
      image: !0,
      hidden: !0,
      radio: !0,
      reset: !0,
      submit: !0
    };
    function Hi(e, t) {
      dc[t.type] || t.onChange || t.onInput || t.readOnly || t.disabled || t.value == null || y("You provided a `value` prop to a form field without an `onChange` handler. This will render a read-only field. If the field should be mutable use `defaultValue`. Otherwise, set either `onChange` or `readOnly`."), t.onChange || t.readOnly || t.disabled || t.checked == null || y("You provided a `checked` prop to a form field without an `onChange` handler. This will render a read-only field. If the field should be mutable use `defaultChecked`. Otherwise, set either `onChange` or `readOnly`.");
    }
    function Cl(e) {
      var t = e.type, a = e.nodeName;
      return a && a.toLowerCase() === "input" && (t === "checkbox" || t === "radio");
    }
    function pc(e) {
      return e._valueTracker;
    }
    function za(e) {
      e._valueTracker = null;
    }
    function El(e) {
      var t = "";
      return e && (Cl(e) ? t = e.checked ? "true" : "false" : t = e.value), t;
    }
    function Pi(e) {
      var t = Cl(e) ? "checked" : "value", a = Object.getOwnPropertyDescriptor(e.constructor.prototype, t);
      Er(e[t]);
      var i = "" + e[t];
      if (!(e.hasOwnProperty(t) || typeof a > "u" || typeof a.get != "function" || typeof a.set != "function")) {
        var o = a.get, s = a.set;
        Object.defineProperty(e, t, {
          configurable: !0,
          get: function() {
            return o.call(this);
          },
          set: function(p) {
            Er(p), i = "" + p, s.call(this, p);
          }
        }), Object.defineProperty(e, t, {
          enumerable: a.enumerable
        });
        var f = {
          getValue: function() {
            return i;
          },
          setValue: function(p) {
            Er(p), i = "" + p;
          },
          stopTracking: function() {
            za(e), delete e[t];
          }
        };
        return f;
      }
    }
    function Aa(e) {
      pc(e) || (e._valueTracker = Pi(e));
    }
    function qo(e) {
      if (!e)
        return !1;
      var t = pc(e);
      if (!t)
        return !0;
      var a = t.getValue(), i = El(e);
      return i !== a ? (t.setValue(i), !0) : !1;
    }
    function wl(e) {
      if (e = e || (typeof document < "u" ? document : void 0), typeof e > "u")
        return null;
      try {
        return e.activeElement || e.body;
      } catch {
        return e.body;
      }
    }
    var Rl = !1, eo = !1, Xo = !1, ns = !1;
    function oi(e) {
      var t = e.type === "checkbox" || e.type === "radio";
      return t ? e.checked != null : e.value != null;
    }
    function h(e, t) {
      var a = e, i = t.checked, o = Et({}, t, {
        defaultChecked: void 0,
        defaultValue: void 0,
        value: void 0,
        checked: i ?? a._wrapperState.initialChecked
      });
      return o;
    }
    function R(e, t) {
      Hi("input", t), t.checked !== void 0 && t.defaultChecked !== void 0 && !eo && (y("%s contains an input of type %s with both checked and defaultChecked props. Input elements must be either controlled or uncontrolled (specify either the checked prop, or the defaultChecked prop, but not both). Decide between using a controlled or uncontrolled input element and remove one of these props. More info: https://reactjs.org/link/controlled-components", Ur() || "A component", t.type), eo = !0), t.value !== void 0 && t.defaultValue !== void 0 && !Rl && (y("%s contains an input of type %s with both value and defaultValue props. Input elements must be either controlled or uncontrolled (specify either the value prop, or the defaultValue prop, but not both). Decide between using a controlled or uncontrolled input element and remove one of these props. More info: https://reactjs.org/link/controlled-components", Ur() || "A component", t.type), Rl = !0);
      var a = e, i = t.defaultValue == null ? "" : t.defaultValue;
      a._wrapperState = {
        initialChecked: t.checked != null ? t.checked : t.defaultChecked,
        initialValue: Ci(t.value != null ? t.value : i),
        controlled: oi(t)
      };
    }
    function F(e, t) {
      var a = e, i = t.checked;
      i != null && xa(a, "checked", i, !1);
    }
    function Y(e, t) {
      var a = e;
      {
        var i = oi(t);
        !a._wrapperState.controlled && i && !ns && (y("A component is changing an uncontrolled input to be controlled. This is likely caused by the value changing from undefined to a defined value, which should not happen. Decide between using a controlled or uncontrolled input element for the lifetime of the component. More info: https://reactjs.org/link/controlled-components"), ns = !0), a._wrapperState.controlled && !i && !Xo && (y("A component is changing a controlled input to be uncontrolled. This is likely caused by the value changing from a defined to undefined, which should not happen. Decide between using a controlled or uncontrolled input element for the lifetime of the component. More info: https://reactjs.org/link/controlled-components"), Xo = !0);
      }
      F(e, t);
      var o = Ci(t.value), s = t.type;
      if (o != null)
        s === "number" ? (o === 0 && a.value === "" || // We explicitly want to coerce to number here if possible.
        // eslint-disable-next-line
        a.value != o) && (a.value = nr(o)) : a.value !== nr(o) && (a.value = nr(o));
      else if (s === "submit" || s === "reset") {
        a.removeAttribute("value");
        return;
      }
      t.hasOwnProperty("value") ? Je(a, t.type, o) : t.hasOwnProperty("defaultValue") && Je(a, t.type, Ci(t.defaultValue)), t.checked == null && t.defaultChecked != null && (a.defaultChecked = !!t.defaultChecked);
    }
    function ue(e, t, a) {
      var i = e;
      if (t.hasOwnProperty("value") || t.hasOwnProperty("defaultValue")) {
        var o = t.type, s = o === "submit" || o === "reset";
        if (s && (t.value === void 0 || t.value === null))
          return;
        var f = nr(i._wrapperState.initialValue);
        a || f !== i.value && (i.value = f), i.defaultValue = f;
      }
      var p = i.name;
      p !== "" && (i.name = ""), i.defaultChecked = !i.defaultChecked, i.defaultChecked = !!i._wrapperState.initialChecked, p !== "" && (i.name = p);
    }
    function et(e, t) {
      var a = e;
      Y(a, t), me(a, t);
    }
    function me(e, t) {
      var a = t.name;
      if (t.type === "radio" && a != null) {
        for (var i = e; i.parentNode; )
          i = i.parentNode;
        Gr(a, "name");
        for (var o = i.querySelectorAll("input[name=" + JSON.stringify("" + a) + '][type="radio"]'), s = 0; s < o.length; s++) {
          var f = o[s];
          if (!(f === e || f.form !== e.form)) {
            var p = Yh(f);
            if (!p)
              throw new Error("ReactDOMInput: Mixing React and non-React radio inputs with the same `name` is not supported.");
            qo(f), Y(f, p);
          }
        }
      }
    }
    function Je(e, t, a) {
      // Focused number inputs synchronize on blur. See ChangeEventPlugin.js
      (t !== "number" || wl(e.ownerDocument) !== e) && (a == null ? e.defaultValue = nr(e._wrapperState.initialValue) : e.defaultValue !== nr(a) && (e.defaultValue = nr(a)));
    }
    var kt = !1, Pt = !1, on = !1;
    function nn(e, t) {
      t.value == null && (typeof t.children == "object" && t.children !== null ? S.Children.forEach(t.children, function(a) {
        a != null && (typeof a == "string" || typeof a == "number" || Pt || (Pt = !0, y("Cannot infer the option value of complex children. Pass a `value` prop or use a plain string as children to <option>.")));
      }) : t.dangerouslySetInnerHTML != null && (on || (on = !0, y("Pass a `value` prop if you set dangerouslyInnerHTML so React knows which value should be selected.")))), t.selected != null && !kt && (y("Use the `defaultValue` or `value` props on <select> instead of setting `selected` on <option>."), kt = !0);
    }
    function un(e, t) {
      t.value != null && e.setAttribute("value", nr(Ci(t.value)));
    }
    var cn = Array.isArray;
    function At(e) {
      return cn(e);
    }
    var Vi;
    Vi = !1;
    function Ko() {
      var e = Ur();
      return e ? `

Check the render method of \`` + e + "`." : "";
    }
    var rs = ["value", "defaultValue"];
    function ld(e) {
      {
        Hi("select", e);
        for (var t = 0; t < rs.length; t++) {
          var a = rs[t];
          if (e[a] != null) {
            var i = At(e[a]);
            e.multiple && !i ? y("The `%s` prop supplied to <select> must be an array if `multiple` is true.%s", a, Ko()) : !e.multiple && i && y("The `%s` prop supplied to <select> must be a scalar value if `multiple` is false.%s", a, Ko());
          }
        }
      }
    }
    function ui(e, t, a, i) {
      var o = e.options;
      if (t) {
        for (var s = a, f = {}, p = 0; p < s.length; p++)
          f["$" + s[p]] = !0;
        for (var v = 0; v < o.length; v++) {
          var g = f.hasOwnProperty("$" + o[v].value);
          o[v].selected !== g && (o[v].selected = g), g && i && (o[v].defaultSelected = !0);
        }
      } else {
        for (var x = nr(Ci(a)), N = null, _ = 0; _ < o.length; _++) {
          if (o[_].value === x) {
            o[_].selected = !0, i && (o[_].defaultSelected = !0);
            return;
          }
          N === null && !o[_].disabled && (N = o[_]);
        }
        N !== null && (N.selected = !0);
      }
    }
    function as(e, t) {
      return Et({}, t, {
        value: void 0
      });
    }
    function is(e, t) {
      var a = e;
      ld(t), a._wrapperState = {
        wasMultiple: !!t.multiple
      }, t.value !== void 0 && t.defaultValue !== void 0 && !Vi && (y("Select elements must be either controlled or uncontrolled (specify either the value prop, or the defaultValue prop, but not both). Decide between using a controlled or uncontrolled select element and remove one of these props. More info: https://reactjs.org/link/controlled-components"), Vi = !0);
    }
    function od(e, t) {
      var a = e;
      a.multiple = !!t.multiple;
      var i = t.value;
      i != null ? ui(a, !!t.multiple, i, !1) : t.defaultValue != null && ui(a, !!t.multiple, t.defaultValue, !0);
    }
    function fy(e, t) {
      var a = e, i = a._wrapperState.wasMultiple;
      a._wrapperState.wasMultiple = !!t.multiple;
      var o = t.value;
      o != null ? ui(a, !!t.multiple, o, !1) : i !== !!t.multiple && (t.defaultValue != null ? ui(a, !!t.multiple, t.defaultValue, !0) : ui(a, !!t.multiple, t.multiple ? [] : "", !1));
    }
    function dy(e, t) {
      var a = e, i = t.value;
      i != null && ui(a, !!t.multiple, i, !1);
    }
    var ud = !1;
    function sd(e, t) {
      var a = e;
      if (t.dangerouslySetInnerHTML != null)
        throw new Error("`dangerouslySetInnerHTML` does not make sense on <textarea>.");
      var i = Et({}, t, {
        value: void 0,
        defaultValue: void 0,
        children: nr(a._wrapperState.initialValue)
      });
      return i;
    }
    function mv(e, t) {
      var a = e;
      Hi("textarea", t), t.value !== void 0 && t.defaultValue !== void 0 && !ud && (y("%s contains a textarea with both value and defaultValue props. Textarea elements must be either controlled or uncontrolled (specify either the value prop, or the defaultValue prop, but not both). Decide between using a controlled or uncontrolled textarea and remove one of these props. More info: https://reactjs.org/link/controlled-components", Ur() || "A component"), ud = !0);
      var i = t.value;
      if (i == null) {
        var o = t.children, s = t.defaultValue;
        if (o != null) {
          y("Use the `defaultValue` or `value` props instead of setting children on <textarea>.");
          {
            if (s != null)
              throw new Error("If you supply `defaultValue` on a <textarea>, do not pass children.");
            if (At(o)) {
              if (o.length > 1)
                throw new Error("<textarea> can only have at most one child.");
              o = o[0];
            }
            s = o;
          }
        }
        s == null && (s = ""), i = s;
      }
      a._wrapperState = {
        initialValue: Ci(i)
      };
    }
    function yv(e, t) {
      var a = e, i = Ci(t.value), o = Ci(t.defaultValue);
      if (i != null) {
        var s = nr(i);
        s !== a.value && (a.value = s), t.defaultValue == null && a.defaultValue !== s && (a.defaultValue = s);
      }
      o != null && (a.defaultValue = nr(o));
    }
    function gv(e, t) {
      var a = e, i = a.textContent;
      i === a._wrapperState.initialValue && i !== "" && i !== null && (a.value = i);
    }
    function cd(e, t) {
      yv(e, t);
    }
    var Bi = "http://www.w3.org/1999/xhtml", py = "http://www.w3.org/1998/Math/MathML", fd = "http://www.w3.org/2000/svg";
    function vc(e) {
      switch (e) {
        case "svg":
          return fd;
        case "math":
          return py;
        default:
          return Bi;
      }
    }
    function dd(e, t) {
      return e == null || e === Bi ? vc(t) : e === fd && t === "foreignObject" ? Bi : e;
    }
    var vy = function(e) {
      return typeof MSApp < "u" && MSApp.execUnsafeLocalFunction ? function(t, a, i, o) {
        MSApp.execUnsafeLocalFunction(function() {
          return e(t, a, i, o);
        });
      } : e;
    }, hc, Sv = vy(function(e, t) {
      if (e.namespaceURI === fd && !("innerHTML" in e)) {
        hc = hc || document.createElement("div"), hc.innerHTML = "<svg>" + t.valueOf().toString() + "</svg>";
        for (var a = hc.firstChild; e.firstChild; )
          e.removeChild(e.firstChild);
        for (; a.firstChild; )
          e.appendChild(a.firstChild);
        return;
      }
      e.innerHTML = t;
    }), ta = 1, $i = 3, Vn = 8, si = 9, to = 11, mc = function(e, t) {
      if (t) {
        var a = e.firstChild;
        if (a && a === e.lastChild && a.nodeType === $i) {
          a.nodeValue = t;
          return;
        }
      }
      e.textContent = t;
    }, xv = {
      animation: ["animationDelay", "animationDirection", "animationDuration", "animationFillMode", "animationIterationCount", "animationName", "animationPlayState", "animationTimingFunction"],
      background: ["backgroundAttachment", "backgroundClip", "backgroundColor", "backgroundImage", "backgroundOrigin", "backgroundPositionX", "backgroundPositionY", "backgroundRepeat", "backgroundSize"],
      backgroundPosition: ["backgroundPositionX", "backgroundPositionY"],
      border: ["borderBottomColor", "borderBottomStyle", "borderBottomWidth", "borderImageOutset", "borderImageRepeat", "borderImageSlice", "borderImageSource", "borderImageWidth", "borderLeftColor", "borderLeftStyle", "borderLeftWidth", "borderRightColor", "borderRightStyle", "borderRightWidth", "borderTopColor", "borderTopStyle", "borderTopWidth"],
      borderBlockEnd: ["borderBlockEndColor", "borderBlockEndStyle", "borderBlockEndWidth"],
      borderBlockStart: ["borderBlockStartColor", "borderBlockStartStyle", "borderBlockStartWidth"],
      borderBottom: ["borderBottomColor", "borderBottomStyle", "borderBottomWidth"],
      borderColor: ["borderBottomColor", "borderLeftColor", "borderRightColor", "borderTopColor"],
      borderImage: ["borderImageOutset", "borderImageRepeat", "borderImageSlice", "borderImageSource", "borderImageWidth"],
      borderInlineEnd: ["borderInlineEndColor", "borderInlineEndStyle", "borderInlineEndWidth"],
      borderInlineStart: ["borderInlineStartColor", "borderInlineStartStyle", "borderInlineStartWidth"],
      borderLeft: ["borderLeftColor", "borderLeftStyle", "borderLeftWidth"],
      borderRadius: ["borderBottomLeftRadius", "borderBottomRightRadius", "borderTopLeftRadius", "borderTopRightRadius"],
      borderRight: ["borderRightColor", "borderRightStyle", "borderRightWidth"],
      borderStyle: ["borderBottomStyle", "borderLeftStyle", "borderRightStyle", "borderTopStyle"],
      borderTop: ["borderTopColor", "borderTopStyle", "borderTopWidth"],
      borderWidth: ["borderBottomWidth", "borderLeftWidth", "borderRightWidth", "borderTopWidth"],
      columnRule: ["columnRuleColor", "columnRuleStyle", "columnRuleWidth"],
      columns: ["columnCount", "columnWidth"],
      flex: ["flexBasis", "flexGrow", "flexShrink"],
      flexFlow: ["flexDirection", "flexWrap"],
      font: ["fontFamily", "fontFeatureSettings", "fontKerning", "fontLanguageOverride", "fontSize", "fontSizeAdjust", "fontStretch", "fontStyle", "fontVariant", "fontVariantAlternates", "fontVariantCaps", "fontVariantEastAsian", "fontVariantLigatures", "fontVariantNumeric", "fontVariantPosition", "fontWeight", "lineHeight"],
      fontVariant: ["fontVariantAlternates", "fontVariantCaps", "fontVariantEastAsian", "fontVariantLigatures", "fontVariantNumeric", "fontVariantPosition"],
      gap: ["columnGap", "rowGap"],
      grid: ["gridAutoColumns", "gridAutoFlow", "gridAutoRows", "gridTemplateAreas", "gridTemplateColumns", "gridTemplateRows"],
      gridArea: ["gridColumnEnd", "gridColumnStart", "gridRowEnd", "gridRowStart"],
      gridColumn: ["gridColumnEnd", "gridColumnStart"],
      gridColumnGap: ["columnGap"],
      gridGap: ["columnGap", "rowGap"],
      gridRow: ["gridRowEnd", "gridRowStart"],
      gridRowGap: ["rowGap"],
      gridTemplate: ["gridTemplateAreas", "gridTemplateColumns", "gridTemplateRows"],
      listStyle: ["listStyleImage", "listStylePosition", "listStyleType"],
      margin: ["marginBottom", "marginLeft", "marginRight", "marginTop"],
      marker: ["markerEnd", "markerMid", "markerStart"],
      mask: ["maskClip", "maskComposite", "maskImage", "maskMode", "maskOrigin", "maskPositionX", "maskPositionY", "maskRepeat", "maskSize"],
      maskPosition: ["maskPositionX", "maskPositionY"],
      outline: ["outlineColor", "outlineStyle", "outlineWidth"],
      overflow: ["overflowX", "overflowY"],
      padding: ["paddingBottom", "paddingLeft", "paddingRight", "paddingTop"],
      placeContent: ["alignContent", "justifyContent"],
      placeItems: ["alignItems", "justifyItems"],
      placeSelf: ["alignSelf", "justifySelf"],
      textDecoration: ["textDecorationColor", "textDecorationLine", "textDecorationStyle"],
      textEmphasis: ["textEmphasisColor", "textEmphasisStyle"],
      transition: ["transitionDelay", "transitionDuration", "transitionProperty", "transitionTimingFunction"],
      wordWrap: ["overflowWrap"]
    }, Jo = {
      animationIterationCount: !0,
      aspectRatio: !0,
      borderImageOutset: !0,
      borderImageSlice: !0,
      borderImageWidth: !0,
      boxFlex: !0,
      boxFlexGroup: !0,
      boxOrdinalGroup: !0,
      columnCount: !0,
      columns: !0,
      flex: !0,
      flexGrow: !0,
      flexPositive: !0,
      flexShrink: !0,
      flexNegative: !0,
      flexOrder: !0,
      gridArea: !0,
      gridRow: !0,
      gridRowEnd: !0,
      gridRowSpan: !0,
      gridRowStart: !0,
      gridColumn: !0,
      gridColumnEnd: !0,
      gridColumnSpan: !0,
      gridColumnStart: !0,
      fontWeight: !0,
      lineClamp: !0,
      lineHeight: !0,
      opacity: !0,
      order: !0,
      orphans: !0,
      tabSize: !0,
      widows: !0,
      zIndex: !0,
      zoom: !0,
      // SVG-related properties
      fillOpacity: !0,
      floodOpacity: !0,
      stopOpacity: !0,
      strokeDasharray: !0,
      strokeDashoffset: !0,
      strokeMiterlimit: !0,
      strokeOpacity: !0,
      strokeWidth: !0
    };
    function bv(e, t) {
      return e + t.charAt(0).toUpperCase() + t.substring(1);
    }
    var Cv = ["Webkit", "ms", "Moz", "O"];
    Object.keys(Jo).forEach(function(e) {
      Cv.forEach(function(t) {
        Jo[bv(t, e)] = Jo[e];
      });
    });
    function yc(e, t, a) {
      var i = t == null || typeof t == "boolean" || t === "";
      return i ? "" : !a && typeof t == "number" && t !== 0 && !(Jo.hasOwnProperty(e) && Jo[e]) ? t + "px" : (Cr(t, e), ("" + t).trim());
    }
    var Zo = /([A-Z])/g, hy = /^ms-/;
    function my(e) {
      return e.replace(Zo, "-$1").toLowerCase().replace(hy, "-ms-");
    }
    var Ev = function() {
    };
    {
      var wv = /^(?:webkit|moz|o)[A-Z]/, Rv = /^-ms-/, ls = /-(.)/g, eu = /;\s*$/, tu = {}, nu = {}, Tv = !1, pd = !1, vd = function(e) {
        return e.replace(ls, function(t, a) {
          return a.toUpperCase();
        });
      }, hd = function(e) {
        tu.hasOwnProperty(e) && tu[e] || (tu[e] = !0, y(
          "Unsupported style property %s. Did you mean %s?",
          e,
          // As Andi Smith suggests
          // (http://www.andismith.com/blog/2012/02/modernizr-prefixed/), an `-ms` prefix
          // is converted to lowercase `ms`.
          vd(e.replace(Rv, "ms-"))
        ));
      }, kv = function(e) {
        tu.hasOwnProperty(e) && tu[e] || (tu[e] = !0, y("Unsupported vendor-prefixed style property %s. Did you mean %s?", e, e.charAt(0).toUpperCase() + e.slice(1)));
      }, _v = function(e, t) {
        nu.hasOwnProperty(t) && nu[t] || (nu[t] = !0, y(`Style property values shouldn't contain a semicolon. Try "%s: %s" instead.`, e, t.replace(eu, "")));
      }, Dv = function(e, t) {
        Tv || (Tv = !0, y("`NaN` is an invalid value for the `%s` css style property.", e));
      }, yy = function(e, t) {
        pd || (pd = !0, y("`Infinity` is an invalid value for the `%s` css style property.", e));
      };
      Ev = function(e, t) {
        e.indexOf("-") > -1 ? hd(e) : wv.test(e) ? kv(e) : eu.test(t) && _v(e, t), typeof t == "number" && (isNaN(t) ? Dv(e, t) : isFinite(t) || yy(e, t));
      };
    }
    var gy = Ev;
    function Sy(e) {
      {
        var t = "", a = "";
        for (var i in e)
          if (e.hasOwnProperty(i)) {
            var o = e[i];
            if (o != null) {
              var s = i.indexOf("--") === 0;
              t += a + (s ? i : my(i)) + ":", t += yc(i, o, s), a = ";";
            }
          }
        return t || null;
      }
    }
    function Nv(e, t) {
      var a = e.style;
      for (var i in t)
        if (t.hasOwnProperty(i)) {
          var o = i.indexOf("--") === 0;
          o || gy(i, t[i]);
          var s = yc(i, t[i], o);
          i === "float" && (i = "cssFloat"), o ? a.setProperty(i, s) : a[i] = s;
        }
    }
    function xy(e) {
      return e == null || typeof e == "boolean" || e === "";
    }
    function Ua(e) {
      var t = {};
      for (var a in e)
        for (var i = xv[a] || [a], o = 0; o < i.length; o++)
          t[i[o]] = a;
      return t;
    }
    function os(e, t) {
      {
        if (!t)
          return;
        var a = Ua(e), i = Ua(t), o = {};
        for (var s in a) {
          var f = a[s], p = i[s];
          if (p && f !== p) {
            var v = f + "," + p;
            if (o[v])
              continue;
            o[v] = !0, y("%s a style property during rerender (%s) when a conflicting property is set (%s) can lead to styling bugs. To avoid this, don't mix shorthand and non-shorthand properties for the same value; instead, replace the shorthand with separate values.", xy(e[f]) ? "Removing" : "Updating", f, p);
          }
        }
      }
    }
    var Ov = {
      area: !0,
      base: !0,
      br: !0,
      col: !0,
      embed: !0,
      hr: !0,
      img: !0,
      input: !0,
      keygen: !0,
      link: !0,
      meta: !0,
      param: !0,
      source: !0,
      track: !0,
      wbr: !0
      // NOTE: menuitem's close tag should be omitted, but that causes problems.
    }, Mv = Et({
      menuitem: !0
    }, Ov), Lv = "__html";
    function gc(e, t) {
      if (t) {
        if (Mv[e] && (t.children != null || t.dangerouslySetInnerHTML != null))
          throw new Error(e + " is a void element tag and must neither have `children` nor use `dangerouslySetInnerHTML`.");
        if (t.dangerouslySetInnerHTML != null) {
          if (t.children != null)
            throw new Error("Can only set one of `children` or `props.dangerouslySetInnerHTML`.");
          if (typeof t.dangerouslySetInnerHTML != "object" || !(Lv in t.dangerouslySetInnerHTML))
            throw new Error("`props.dangerouslySetInnerHTML` must be in the form `{__html: ...}`. Please visit https://reactjs.org/link/dangerously-set-inner-html for more information.");
        }
        if (!t.suppressContentEditableWarning && t.contentEditable && t.children != null && y("A component is `contentEditable` and contains `children` managed by React. It is now your responsibility to guarantee that none of those nodes are unexpectedly modified or duplicated. This is probably not intentional."), t.style != null && typeof t.style != "object")
          throw new Error("The `style` prop expects a mapping from style properties to values, not a string. For example, style={{marginRight: spacing + 'em'}} when using JSX.");
      }
    }
    function Ii(e, t) {
      if (e.indexOf("-") === -1)
        return typeof t.is == "string";
      switch (e) {
        case "annotation-xml":
        case "color-profile":
        case "font-face":
        case "font-face-src":
        case "font-face-uri":
        case "font-face-format":
        case "font-face-name":
        case "missing-glyph":
          return !1;
        default:
          return !0;
      }
    }
    var Sc = {
      // HTML
      accept: "accept",
      acceptcharset: "acceptCharset",
      "accept-charset": "acceptCharset",
      accesskey: "accessKey",
      action: "action",
      allowfullscreen: "allowFullScreen",
      alt: "alt",
      as: "as",
      async: "async",
      autocapitalize: "autoCapitalize",
      autocomplete: "autoComplete",
      autocorrect: "autoCorrect",
      autofocus: "autoFocus",
      autoplay: "autoPlay",
      autosave: "autoSave",
      capture: "capture",
      cellpadding: "cellPadding",
      cellspacing: "cellSpacing",
      challenge: "challenge",
      charset: "charSet",
      checked: "checked",
      children: "children",
      cite: "cite",
      class: "className",
      classid: "classID",
      classname: "className",
      cols: "cols",
      colspan: "colSpan",
      content: "content",
      contenteditable: "contentEditable",
      contextmenu: "contextMenu",
      controls: "controls",
      controlslist: "controlsList",
      coords: "coords",
      crossorigin: "crossOrigin",
      dangerouslysetinnerhtml: "dangerouslySetInnerHTML",
      data: "data",
      datetime: "dateTime",
      default: "default",
      defaultchecked: "defaultChecked",
      defaultvalue: "defaultValue",
      defer: "defer",
      dir: "dir",
      disabled: "disabled",
      disablepictureinpicture: "disablePictureInPicture",
      disableremoteplayback: "disableRemotePlayback",
      download: "download",
      draggable: "draggable",
      enctype: "encType",
      enterkeyhint: "enterKeyHint",
      for: "htmlFor",
      form: "form",
      formmethod: "formMethod",
      formaction: "formAction",
      formenctype: "formEncType",
      formnovalidate: "formNoValidate",
      formtarget: "formTarget",
      frameborder: "frameBorder",
      headers: "headers",
      height: "height",
      hidden: "hidden",
      high: "high",
      href: "href",
      hreflang: "hrefLang",
      htmlfor: "htmlFor",
      httpequiv: "httpEquiv",
      "http-equiv": "httpEquiv",
      icon: "icon",
      id: "id",
      imagesizes: "imageSizes",
      imagesrcset: "imageSrcSet",
      innerhtml: "innerHTML",
      inputmode: "inputMode",
      integrity: "integrity",
      is: "is",
      itemid: "itemID",
      itemprop: "itemProp",
      itemref: "itemRef",
      itemscope: "itemScope",
      itemtype: "itemType",
      keyparams: "keyParams",
      keytype: "keyType",
      kind: "kind",
      label: "label",
      lang: "lang",
      list: "list",
      loop: "loop",
      low: "low",
      manifest: "manifest",
      marginwidth: "marginWidth",
      marginheight: "marginHeight",
      max: "max",
      maxlength: "maxLength",
      media: "media",
      mediagroup: "mediaGroup",
      method: "method",
      min: "min",
      minlength: "minLength",
      multiple: "multiple",
      muted: "muted",
      name: "name",
      nomodule: "noModule",
      nonce: "nonce",
      novalidate: "noValidate",
      open: "open",
      optimum: "optimum",
      pattern: "pattern",
      placeholder: "placeholder",
      playsinline: "playsInline",
      poster: "poster",
      preload: "preload",
      profile: "profile",
      radiogroup: "radioGroup",
      readonly: "readOnly",
      referrerpolicy: "referrerPolicy",
      rel: "rel",
      required: "required",
      reversed: "reversed",
      role: "role",
      rows: "rows",
      rowspan: "rowSpan",
      sandbox: "sandbox",
      scope: "scope",
      scoped: "scoped",
      scrolling: "scrolling",
      seamless: "seamless",
      selected: "selected",
      shape: "shape",
      size: "size",
      sizes: "sizes",
      span: "span",
      spellcheck: "spellCheck",
      src: "src",
      srcdoc: "srcDoc",
      srclang: "srcLang",
      srcset: "srcSet",
      start: "start",
      step: "step",
      style: "style",
      summary: "summary",
      tabindex: "tabIndex",
      target: "target",
      title: "title",
      type: "type",
      usemap: "useMap",
      value: "value",
      width: "width",
      wmode: "wmode",
      wrap: "wrap",
      // SVG
      about: "about",
      accentheight: "accentHeight",
      "accent-height": "accentHeight",
      accumulate: "accumulate",
      additive: "additive",
      alignmentbaseline: "alignmentBaseline",
      "alignment-baseline": "alignmentBaseline",
      allowreorder: "allowReorder",
      alphabetic: "alphabetic",
      amplitude: "amplitude",
      arabicform: "arabicForm",
      "arabic-form": "arabicForm",
      ascent: "ascent",
      attributename: "attributeName",
      attributetype: "attributeType",
      autoreverse: "autoReverse",
      azimuth: "azimuth",
      basefrequency: "baseFrequency",
      baselineshift: "baselineShift",
      "baseline-shift": "baselineShift",
      baseprofile: "baseProfile",
      bbox: "bbox",
      begin: "begin",
      bias: "bias",
      by: "by",
      calcmode: "calcMode",
      capheight: "capHeight",
      "cap-height": "capHeight",
      clip: "clip",
      clippath: "clipPath",
      "clip-path": "clipPath",
      clippathunits: "clipPathUnits",
      cliprule: "clipRule",
      "clip-rule": "clipRule",
      color: "color",
      colorinterpolation: "colorInterpolation",
      "color-interpolation": "colorInterpolation",
      colorinterpolationfilters: "colorInterpolationFilters",
      "color-interpolation-filters": "colorInterpolationFilters",
      colorprofile: "colorProfile",
      "color-profile": "colorProfile",
      colorrendering: "colorRendering",
      "color-rendering": "colorRendering",
      contentscripttype: "contentScriptType",
      contentstyletype: "contentStyleType",
      cursor: "cursor",
      cx: "cx",
      cy: "cy",
      d: "d",
      datatype: "datatype",
      decelerate: "decelerate",
      descent: "descent",
      diffuseconstant: "diffuseConstant",
      direction: "direction",
      display: "display",
      divisor: "divisor",
      dominantbaseline: "dominantBaseline",
      "dominant-baseline": "dominantBaseline",
      dur: "dur",
      dx: "dx",
      dy: "dy",
      edgemode: "edgeMode",
      elevation: "elevation",
      enablebackground: "enableBackground",
      "enable-background": "enableBackground",
      end: "end",
      exponent: "exponent",
      externalresourcesrequired: "externalResourcesRequired",
      fill: "fill",
      fillopacity: "fillOpacity",
      "fill-opacity": "fillOpacity",
      fillrule: "fillRule",
      "fill-rule": "fillRule",
      filter: "filter",
      filterres: "filterRes",
      filterunits: "filterUnits",
      floodopacity: "floodOpacity",
      "flood-opacity": "floodOpacity",
      floodcolor: "floodColor",
      "flood-color": "floodColor",
      focusable: "focusable",
      fontfamily: "fontFamily",
      "font-family": "fontFamily",
      fontsize: "fontSize",
      "font-size": "fontSize",
      fontsizeadjust: "fontSizeAdjust",
      "font-size-adjust": "fontSizeAdjust",
      fontstretch: "fontStretch",
      "font-stretch": "fontStretch",
      fontstyle: "fontStyle",
      "font-style": "fontStyle",
      fontvariant: "fontVariant",
      "font-variant": "fontVariant",
      fontweight: "fontWeight",
      "font-weight": "fontWeight",
      format: "format",
      from: "from",
      fx: "fx",
      fy: "fy",
      g1: "g1",
      g2: "g2",
      glyphname: "glyphName",
      "glyph-name": "glyphName",
      glyphorientationhorizontal: "glyphOrientationHorizontal",
      "glyph-orientation-horizontal": "glyphOrientationHorizontal",
      glyphorientationvertical: "glyphOrientationVertical",
      "glyph-orientation-vertical": "glyphOrientationVertical",
      glyphref: "glyphRef",
      gradienttransform: "gradientTransform",
      gradientunits: "gradientUnits",
      hanging: "hanging",
      horizadvx: "horizAdvX",
      "horiz-adv-x": "horizAdvX",
      horizoriginx: "horizOriginX",
      "horiz-origin-x": "horizOriginX",
      ideographic: "ideographic",
      imagerendering: "imageRendering",
      "image-rendering": "imageRendering",
      in2: "in2",
      in: "in",
      inlist: "inlist",
      intercept: "intercept",
      k1: "k1",
      k2: "k2",
      k3: "k3",
      k4: "k4",
      k: "k",
      kernelmatrix: "kernelMatrix",
      kernelunitlength: "kernelUnitLength",
      kerning: "kerning",
      keypoints: "keyPoints",
      keysplines: "keySplines",
      keytimes: "keyTimes",
      lengthadjust: "lengthAdjust",
      letterspacing: "letterSpacing",
      "letter-spacing": "letterSpacing",
      lightingcolor: "lightingColor",
      "lighting-color": "lightingColor",
      limitingconeangle: "limitingConeAngle",
      local: "local",
      markerend: "markerEnd",
      "marker-end": "markerEnd",
      markerheight: "markerHeight",
      markermid: "markerMid",
      "marker-mid": "markerMid",
      markerstart: "markerStart",
      "marker-start": "markerStart",
      markerunits: "markerUnits",
      markerwidth: "markerWidth",
      mask: "mask",
      maskcontentunits: "maskContentUnits",
      maskunits: "maskUnits",
      mathematical: "mathematical",
      mode: "mode",
      numoctaves: "numOctaves",
      offset: "offset",
      opacity: "opacity",
      operator: "operator",
      order: "order",
      orient: "orient",
      orientation: "orientation",
      origin: "origin",
      overflow: "overflow",
      overlineposition: "overlinePosition",
      "overline-position": "overlinePosition",
      overlinethickness: "overlineThickness",
      "overline-thickness": "overlineThickness",
      paintorder: "paintOrder",
      "paint-order": "paintOrder",
      panose1: "panose1",
      "panose-1": "panose1",
      pathlength: "pathLength",
      patterncontentunits: "patternContentUnits",
      patterntransform: "patternTransform",
      patternunits: "patternUnits",
      pointerevents: "pointerEvents",
      "pointer-events": "pointerEvents",
      points: "points",
      pointsatx: "pointsAtX",
      pointsaty: "pointsAtY",
      pointsatz: "pointsAtZ",
      prefix: "prefix",
      preservealpha: "preserveAlpha",
      preserveaspectratio: "preserveAspectRatio",
      primitiveunits: "primitiveUnits",
      property: "property",
      r: "r",
      radius: "radius",
      refx: "refX",
      refy: "refY",
      renderingintent: "renderingIntent",
      "rendering-intent": "renderingIntent",
      repeatcount: "repeatCount",
      repeatdur: "repeatDur",
      requiredextensions: "requiredExtensions",
      requiredfeatures: "requiredFeatures",
      resource: "resource",
      restart: "restart",
      result: "result",
      results: "results",
      rotate: "rotate",
      rx: "rx",
      ry: "ry",
      scale: "scale",
      security: "security",
      seed: "seed",
      shaperendering: "shapeRendering",
      "shape-rendering": "shapeRendering",
      slope: "slope",
      spacing: "spacing",
      specularconstant: "specularConstant",
      specularexponent: "specularExponent",
      speed: "speed",
      spreadmethod: "spreadMethod",
      startoffset: "startOffset",
      stddeviation: "stdDeviation",
      stemh: "stemh",
      stemv: "stemv",
      stitchtiles: "stitchTiles",
      stopcolor: "stopColor",
      "stop-color": "stopColor",
      stopopacity: "stopOpacity",
      "stop-opacity": "stopOpacity",
      strikethroughposition: "strikethroughPosition",
      "strikethrough-position": "strikethroughPosition",
      strikethroughthickness: "strikethroughThickness",
      "strikethrough-thickness": "strikethroughThickness",
      string: "string",
      stroke: "stroke",
      strokedasharray: "strokeDasharray",
      "stroke-dasharray": "strokeDasharray",
      strokedashoffset: "strokeDashoffset",
      "stroke-dashoffset": "strokeDashoffset",
      strokelinecap: "strokeLinecap",
      "stroke-linecap": "strokeLinecap",
      strokelinejoin: "strokeLinejoin",
      "stroke-linejoin": "strokeLinejoin",
      strokemiterlimit: "strokeMiterlimit",
      "stroke-miterlimit": "strokeMiterlimit",
      strokewidth: "strokeWidth",
      "stroke-width": "strokeWidth",
      strokeopacity: "strokeOpacity",
      "stroke-opacity": "strokeOpacity",
      suppresscontenteditablewarning: "suppressContentEditableWarning",
      suppresshydrationwarning: "suppressHydrationWarning",
      surfacescale: "surfaceScale",
      systemlanguage: "systemLanguage",
      tablevalues: "tableValues",
      targetx: "targetX",
      targety: "targetY",
      textanchor: "textAnchor",
      "text-anchor": "textAnchor",
      textdecoration: "textDecoration",
      "text-decoration": "textDecoration",
      textlength: "textLength",
      textrendering: "textRendering",
      "text-rendering": "textRendering",
      to: "to",
      transform: "transform",
      typeof: "typeof",
      u1: "u1",
      u2: "u2",
      underlineposition: "underlinePosition",
      "underline-position": "underlinePosition",
      underlinethickness: "underlineThickness",
      "underline-thickness": "underlineThickness",
      unicode: "unicode",
      unicodebidi: "unicodeBidi",
      "unicode-bidi": "unicodeBidi",
      unicoderange: "unicodeRange",
      "unicode-range": "unicodeRange",
      unitsperem: "unitsPerEm",
      "units-per-em": "unitsPerEm",
      unselectable: "unselectable",
      valphabetic: "vAlphabetic",
      "v-alphabetic": "vAlphabetic",
      values: "values",
      vectoreffect: "vectorEffect",
      "vector-effect": "vectorEffect",
      version: "version",
      vertadvy: "vertAdvY",
      "vert-adv-y": "vertAdvY",
      vertoriginx: "vertOriginX",
      "vert-origin-x": "vertOriginX",
      vertoriginy: "vertOriginY",
      "vert-origin-y": "vertOriginY",
      vhanging: "vHanging",
      "v-hanging": "vHanging",
      videographic: "vIdeographic",
      "v-ideographic": "vIdeographic",
      viewbox: "viewBox",
      viewtarget: "viewTarget",
      visibility: "visibility",
      vmathematical: "vMathematical",
      "v-mathematical": "vMathematical",
      vocab: "vocab",
      widths: "widths",
      wordspacing: "wordSpacing",
      "word-spacing": "wordSpacing",
      writingmode: "writingMode",
      "writing-mode": "writingMode",
      x1: "x1",
      x2: "x2",
      x: "x",
      xchannelselector: "xChannelSelector",
      xheight: "xHeight",
      "x-height": "xHeight",
      xlinkactuate: "xlinkActuate",
      "xlink:actuate": "xlinkActuate",
      xlinkarcrole: "xlinkArcrole",
      "xlink:arcrole": "xlinkArcrole",
      xlinkhref: "xlinkHref",
      "xlink:href": "xlinkHref",
      xlinkrole: "xlinkRole",
      "xlink:role": "xlinkRole",
      xlinkshow: "xlinkShow",
      "xlink:show": "xlinkShow",
      xlinktitle: "xlinkTitle",
      "xlink:title": "xlinkTitle",
      xlinktype: "xlinkType",
      "xlink:type": "xlinkType",
      xmlbase: "xmlBase",
      "xml:base": "xmlBase",
      xmllang: "xmlLang",
      "xml:lang": "xmlLang",
      xmlns: "xmlns",
      "xml:space": "xmlSpace",
      xmlnsxlink: "xmlnsXlink",
      "xmlns:xlink": "xmlnsXlink",
      xmlspace: "xmlSpace",
      y1: "y1",
      y2: "y2",
      y: "y",
      ychannelselector: "yChannelSelector",
      z: "z",
      zoomandpan: "zoomAndPan"
    }, jv = {
      "aria-current": 0,
      // state
      "aria-description": 0,
      "aria-details": 0,
      "aria-disabled": 0,
      // state
      "aria-hidden": 0,
      // state
      "aria-invalid": 0,
      // state
      "aria-keyshortcuts": 0,
      "aria-label": 0,
      "aria-roledescription": 0,
      // Widget Attributes
      "aria-autocomplete": 0,
      "aria-checked": 0,
      "aria-expanded": 0,
      "aria-haspopup": 0,
      "aria-level": 0,
      "aria-modal": 0,
      "aria-multiline": 0,
      "aria-multiselectable": 0,
      "aria-orientation": 0,
      "aria-placeholder": 0,
      "aria-pressed": 0,
      "aria-readonly": 0,
      "aria-required": 0,
      "aria-selected": 0,
      "aria-sort": 0,
      "aria-valuemax": 0,
      "aria-valuemin": 0,
      "aria-valuenow": 0,
      "aria-valuetext": 0,
      // Live Region Attributes
      "aria-atomic": 0,
      "aria-busy": 0,
      "aria-live": 0,
      "aria-relevant": 0,
      // Drag-and-Drop Attributes
      "aria-dropeffect": 0,
      "aria-grabbed": 0,
      // Relationship Attributes
      "aria-activedescendant": 0,
      "aria-colcount": 0,
      "aria-colindex": 0,
      "aria-colspan": 0,
      "aria-controls": 0,
      "aria-describedby": 0,
      "aria-errormessage": 0,
      "aria-flowto": 0,
      "aria-labelledby": 0,
      "aria-owns": 0,
      "aria-posinset": 0,
      "aria-rowcount": 0,
      "aria-rowindex": 0,
      "aria-rowspan": 0,
      "aria-setsize": 0
    }, ci = {}, md = new RegExp("^(aria)-[" + We + "]*$"), us = new RegExp("^(aria)[A-Z][" + We + "]*$");
    function yd(e, t) {
      {
        if (Zn.call(ci, t) && ci[t])
          return !0;
        if (us.test(t)) {
          var a = "aria-" + t.slice(4).toLowerCase(), i = jv.hasOwnProperty(a) ? a : null;
          if (i == null)
            return y("Invalid ARIA attribute `%s`. ARIA attributes follow the pattern aria-* and must be lowercase.", t), ci[t] = !0, !0;
          if (t !== i)
            return y("Invalid ARIA attribute `%s`. Did you mean `%s`?", t, i), ci[t] = !0, !0;
        }
        if (md.test(t)) {
          var o = t.toLowerCase(), s = jv.hasOwnProperty(o) ? o : null;
          if (s == null)
            return ci[t] = !0, !1;
          if (t !== s)
            return y("Unknown ARIA attribute `%s`. Did you mean `%s`?", t, s), ci[t] = !0, !0;
        }
      }
      return !0;
    }
    function zv(e, t) {
      {
        var a = [];
        for (var i in t) {
          var o = yd(e, i);
          o || a.push(i);
        }
        var s = a.map(function(f) {
          return "`" + f + "`";
        }).join(", ");
        a.length === 1 ? y("Invalid aria prop %s on <%s> tag. For details, see https://reactjs.org/link/invalid-aria-props", s, e) : a.length > 1 && y("Invalid aria props %s on <%s> tag. For details, see https://reactjs.org/link/invalid-aria-props", s, e);
      }
    }
    function xc(e, t) {
      Ii(e, t) || zv(e, t);
    }
    var no = !1;
    function gd(e, t) {
      {
        if (e !== "input" && e !== "textarea" && e !== "select")
          return;
        t != null && t.value === null && !no && (no = !0, e === "select" && t.multiple ? y("`value` prop on `%s` should not be null. Consider using an empty array when `multiple` is set to `true` to clear the component or `undefined` for uncontrolled components.", e) : y("`value` prop on `%s` should not be null. Consider using an empty string to clear the component or `undefined` for uncontrolled components.", e));
      }
    }
    var Sd = function() {
    };
    {
      var rr = {}, xd = /^on./, Av = /^on[^A-Z]/, Uv = new RegExp("^(aria)-[" + We + "]*$"), Fv = new RegExp("^(aria)[A-Z][" + We + "]*$");
      Sd = function(e, t, a, i) {
        if (Zn.call(rr, t) && rr[t])
          return !0;
        var o = t.toLowerCase();
        if (o === "onfocusin" || o === "onfocusout")
          return y("React uses onFocus and onBlur instead of onFocusIn and onFocusOut. All React events are normalized to bubble, so onFocusIn and onFocusOut are not needed/supported by React."), rr[t] = !0, !0;
        if (i != null) {
          var s = i.registrationNameDependencies, f = i.possibleRegistrationNames;
          if (s.hasOwnProperty(t))
            return !0;
          var p = f.hasOwnProperty(o) ? f[o] : null;
          if (p != null)
            return y("Invalid event handler property `%s`. Did you mean `%s`?", t, p), rr[t] = !0, !0;
          if (xd.test(t))
            return y("Unknown event handler property `%s`. It will be ignored.", t), rr[t] = !0, !0;
        } else if (xd.test(t))
          return Av.test(t) && y("Invalid event handler property `%s`. React events use the camelCase naming convention, for example `onClick`.", t), rr[t] = !0, !0;
        if (Uv.test(t) || Fv.test(t))
          return !0;
        if (o === "innerhtml")
          return y("Directly setting property `innerHTML` is not permitted. For more information, lookup documentation on `dangerouslySetInnerHTML`."), rr[t] = !0, !0;
        if (o === "aria")
          return y("The `aria` attribute is reserved for future use in React. Pass individual `aria-` attributes instead."), rr[t] = !0, !0;
        if (o === "is" && a !== null && a !== void 0 && typeof a != "string")
          return y("Received a `%s` for a string attribute `is`. If this is expected, cast the value to a string.", typeof a), rr[t] = !0, !0;
        if (typeof a == "number" && isNaN(a))
          return y("Received NaN for the `%s` attribute. If this is expected, cast the value to a string.", t), rr[t] = !0, !0;
        var v = Mr(t), g = v !== null && v.type === ya;
        if (Sc.hasOwnProperty(o)) {
          var x = Sc[o];
          if (x !== t)
            return y("Invalid DOM property `%s`. Did you mean `%s`?", t, x), rr[t] = !0, !0;
        } else if (!g && t !== o)
          return y("React does not recognize the `%s` prop on a DOM element. If you intentionally want it to appear in the DOM as a custom attribute, spell it as lowercase `%s` instead. If you accidentally passed it from a parent component, remove it from the DOM element.", t, o), rr[t] = !0, !0;
        return typeof a == "boolean" && wr(t, a, v, !1) ? (a ? y('Received `%s` for a non-boolean attribute `%s`.\n\nIf you want to write it to the DOM, pass a string instead: %s="%s" or %s={value.toString()}.', a, t, t, a, t) : y('Received `%s` for a non-boolean attribute `%s`.\n\nIf you want to write it to the DOM, pass a string instead: %s="%s" or %s={value.toString()}.\n\nIf you used to conditionally omit it with %s={condition && value}, pass %s={condition ? value : undefined} instead.', a, t, t, a, t, t, t), rr[t] = !0, !0) : g ? !0 : wr(t, a, v, !1) ? (rr[t] = !0, !1) : ((a === "false" || a === "true") && v !== null && v.type === bn && (y("Received the string `%s` for the boolean attribute `%s`. %s Did you mean %s={%s}?", a, t, a === "false" ? "The browser will interpret it as a truthy value." : 'Although this works, it will not work as expected if you pass the string "false".', t, a), rr[t] = !0), !0);
      };
    }
    var Hv = function(e, t, a) {
      {
        var i = [];
        for (var o in t) {
          var s = Sd(e, o, t[o], a);
          s || i.push(o);
        }
        var f = i.map(function(p) {
          return "`" + p + "`";
        }).join(", ");
        i.length === 1 ? y("Invalid value for prop %s on <%s> tag. Either remove it from the element, or pass a string or number value to keep it in the DOM. For details, see https://reactjs.org/link/attribute-behavior ", f, e) : i.length > 1 && y("Invalid values for props %s on <%s> tag. Either remove them from the element, or pass a string or number value to keep them in the DOM. For details, see https://reactjs.org/link/attribute-behavior ", f, e);
      }
    };
    function Pv(e, t, a) {
      Ii(e, t) || Hv(e, t, a);
    }
    var Yi = 1, ss = 2, ro = 4, by = Yi | ss | ro, cs = null;
    function fs(e) {
      cs !== null && y("Expected currently replaying event to be null. This error is likely caused by a bug in React. Please file an issue."), cs = e;
    }
    function Cy() {
      cs === null && y("Expected currently replaying event to not be null. This error is likely caused by a bug in React. Please file an issue."), cs = null;
    }
    function Vv(e) {
      return e === cs;
    }
    function bc(e) {
      var t = e.target || e.srcElement || window;
      return t.correspondingUseElement && (t = t.correspondingUseElement), t.nodeType === $i ? t.parentNode : t;
    }
    var sn = null, Tl = null, Wi = null;
    function ru(e) {
      var t = Au(e);
      if (t) {
        if (typeof sn != "function")
          throw new Error("setRestoreImplementation() needs to be called to handle a target for controlled events. This error is likely caused by a bug in React. Please file an issue.");
        var a = t.stateNode;
        if (a) {
          var i = Yh(a);
          sn(t.stateNode, t.type, i);
        }
      }
    }
    function Bv(e) {
      sn = e;
    }
    function Cc(e) {
      Tl ? Wi ? Wi.push(e) : Wi = [e] : Tl = e;
    }
    function ds() {
      return Tl !== null || Wi !== null;
    }
    function ps() {
      if (Tl) {
        var e = Tl, t = Wi;
        if (Tl = null, Wi = null, ru(e), t)
          for (var a = 0; a < t.length; a++)
            ru(t[a]);
      }
    }
    var ao = function(e, t) {
      return e(t);
    }, bd = function() {
    }, Cd = !1;
    function Ey() {
      var e = ds();
      e && (bd(), ps());
    }
    function Ed(e, t, a) {
      if (Cd)
        return e(t, a);
      Cd = !0;
      try {
        return ao(e, t, a);
      } finally {
        Cd = !1, Ey();
      }
    }
    function Ec(e, t, a) {
      ao = e, bd = a;
    }
    function wc(e) {
      return e === "button" || e === "input" || e === "select" || e === "textarea";
    }
    function wd(e, t, a) {
      switch (e) {
        case "onClick":
        case "onClickCapture":
        case "onDoubleClick":
        case "onDoubleClickCapture":
        case "onMouseDown":
        case "onMouseDownCapture":
        case "onMouseMove":
        case "onMouseMoveCapture":
        case "onMouseUp":
        case "onMouseUpCapture":
        case "onMouseEnter":
          return !!(a.disabled && wc(t));
        default:
          return !1;
      }
    }
    function io(e, t) {
      var a = e.stateNode;
      if (a === null)
        return null;
      var i = Yh(a);
      if (i === null)
        return null;
      var o = i[t];
      if (wd(t, e.type, i))
        return null;
      if (o && typeof o != "function")
        throw new Error("Expected `" + t + "` listener to be a function, instead got a value of `" + typeof o + "` type.");
      return o;
    }
    var vs = !1;
    if (xn)
      try {
        var lo = {};
        Object.defineProperty(lo, "passive", {
          get: function() {
            vs = !0;
          }
        }), window.addEventListener("test", lo, lo), window.removeEventListener("test", lo, lo);
      } catch {
        vs = !1;
      }
    function $v(e, t, a, i, o, s, f, p, v) {
      var g = Array.prototype.slice.call(arguments, 3);
      try {
        t.apply(a, g);
      } catch (x) {
        this.onError(x);
      }
    }
    var Rd = $v;
    if (typeof window < "u" && typeof window.dispatchEvent == "function" && typeof document < "u" && typeof document.createEvent == "function") {
      var Td = document.createElement("react");
      Rd = function(t, a, i, o, s, f, p, v, g) {
        if (typeof document > "u" || document === null)
          throw new Error("The `document` globalThis was defined when React was initialized, but is not defined anymore. This can happen in a test environment if a component schedules an update from an asynchronous callback, but the test has already finished running. To solve this, you can either unmount the component at the end of your test (and ensure that any asynchronous operations get canceled in `componentWillUnmount`), or you can change the test itself to be asynchronous.");
        var x = document.createEvent("Event"), N = !1, _ = !0, A = window.event, P = Object.getOwnPropertyDescriptor(window, "event");
        function Q() {
          Td.removeEventListener(G, Xe, !1), typeof window.event < "u" && window.hasOwnProperty("event") && (window.event = A);
        }
        var ge = Array.prototype.slice.call(arguments, 3);
        function Xe() {
          N = !0, Q(), a.apply(i, ge), _ = !1;
        }
        var Be, Ht = !1, Mt = !1;
        function L(j) {
          if (Be = j.error, Ht = !0, Be === null && j.colno === 0 && j.lineno === 0 && (Mt = !0), j.defaultPrevented && Be != null && typeof Be == "object")
            try {
              Be._suppressLogging = !0;
            } catch {
            }
        }
        var G = "react-" + (t || "invokeguardedcallback");
        if (window.addEventListener("error", L), Td.addEventListener(G, Xe, !1), x.initEvent(G, !1, !1), Td.dispatchEvent(x), P && Object.defineProperty(window, "event", P), N && _ && (Ht ? Mt && (Be = new Error("A cross-origin error was thrown. React doesn't have access to the actual error object in development. See https://reactjs.org/link/crossorigin-error for more information.")) : Be = new Error(`An error was thrown inside one of your components, but React doesn't know what it was. This is likely due to browser flakiness. React does its best to preserve the "Pause on exceptions" behavior of the DevTools, which requires some DEV-mode only tricks. It's possible that these don't work in your browser. Try triggering the error in production mode, or switching to a modern browser. If you suspect that this is actually an issue with React, please file an issue.`), this.onError(Be)), window.removeEventListener("error", L), !N)
          return Q(), $v.apply(this, arguments);
      };
    }
    var wy = Rd, kl = !1, fi = null, hs = !1, _l = null, Ei = {
      onError: function(e) {
        kl = !0, fi = e;
      }
    };
    function oo(e, t, a, i, o, s, f, p, v) {
      kl = !1, fi = null, wy.apply(Ei, arguments);
    }
    function Qi(e, t, a, i, o, s, f, p, v) {
      if (oo.apply(this, arguments), kl) {
        var g = _d();
        hs || (hs = !0, _l = g);
      }
    }
    function kd() {
      if (hs) {
        var e = _l;
        throw hs = !1, _l = null, e;
      }
    }
    function Ry() {
      return kl;
    }
    function _d() {
      if (kl) {
        var e = fi;
        return kl = !1, fi = null, e;
      } else
        throw new Error("clearCaughtError was called but no error was captured. This error is likely caused by a bug in React. Please file an issue.");
    }
    function Fa(e) {
      return e._reactInternals;
    }
    function ms(e) {
      return e._reactInternals !== void 0;
    }
    function au(e, t) {
      e._reactInternals = t;
    }
    var qe = (
      /*                      */
      0
    ), Dl = (
      /*                */
      1
    ), pn = (
      /*                    */
      2
    ), xt = (
      /*                       */
      4
    ), Gt = (
      /*                */
      16
    ), Zt = (
      /*                 */
      32
    ), wi = (
      /*                     */
      64
    ), ot = (
      /*                   */
      128
    ), _n = (
      /*            */
      256
    ), na = (
      /*                          */
      512
    ), Ha = (
      /*                     */
      1024
    ), yn = (
      /*                      */
      2048
    ), Pa = (
      /*                    */
      4096
    ), Nl = (
      /*                   */
      8192
    ), ys = (
      /*             */
      16384
    ), Rc = yn | xt | wi | na | Ha | ys, Iv = (
      /*               */
      32767
    ), Ca = (
      /*                   */
      32768
    ), ar = (
      /*                */
      65536
    ), gs = (
      /* */
      131072
    ), Dd = (
      /*                       */
      1048576
    ), Nd = (
      /*                    */
      2097152
    ), ra = (
      /*                 */
      4194304
    ), Ol = (
      /*                */
      8388608
    ), aa = (
      /*               */
      16777216
    ), uo = (
      /*              */
      33554432
    ), iu = (
      // TODO: Remove Update flag from before mutation phase by re-landing Visibility
      // flag logic (see #20043)
      xt | Ha | 0
    ), ia = pn | xt | Gt | Zt | na | Pa | Nl, Tr = xt | wi | na | Nl, Va = yn | Gt, cr = ra | Ol | Nd, Gi = b.ReactCurrentOwner;
    function Ea(e) {
      var t = e, a = e;
      if (e.alternate)
        for (; t.return; )
          t = t.return;
      else {
        var i = t;
        do
          t = i, (t.flags & (pn | Pa)) !== qe && (a = t.return), i = t.return;
        while (i);
      }
      return t.tag === ne ? a : null;
    }
    function Od(e) {
      if (e.tag === ke) {
        var t = e.memoizedState;
        if (t === null) {
          var a = e.alternate;
          a !== null && (t = a.memoizedState);
        }
        if (t !== null)
          return t.dehydrated;
      }
      return null;
    }
    function Tc(e) {
      return e.tag === ne ? e.stateNode.containerInfo : null;
    }
    function Md(e) {
      return Ea(e) === e;
    }
    function wa(e) {
      {
        var t = Gi.current;
        if (t !== null && t.tag === K) {
          var a = t, i = a.stateNode;
          i._warnedAboutRefsInRender || y("%s is accessing isMounted inside its render() function. render() should be a pure function of props and state. It should never access something that requires stale data from the previous render, such as refs. Move this logic to componentDidMount and componentDidUpdate instead.", dt(a) || "A component"), i._warnedAboutRefsInRender = !0;
        }
      }
      var o = Fa(e);
      return o ? Ea(o) === o : !1;
    }
    function la(e) {
      if (Ea(e) !== e)
        throw new Error("Unable to find node on an unmounted component.");
    }
    function vn(e) {
      var t = e.alternate;
      if (!t) {
        var a = Ea(e);
        if (a === null)
          throw new Error("Unable to find node on an unmounted component.");
        return a !== e ? null : e;
      }
      for (var i = e, o = t; ; ) {
        var s = i.return;
        if (s === null)
          break;
        var f = s.alternate;
        if (f === null) {
          var p = s.return;
          if (p !== null) {
            i = o = p;
            continue;
          }
          break;
        }
        if (s.child === f.child) {
          for (var v = s.child; v; ) {
            if (v === i)
              return la(s), e;
            if (v === o)
              return la(s), t;
            v = v.sibling;
          }
          throw new Error("Unable to find node on an unmounted component.");
        }
        if (i.return !== o.return)
          i = s, o = f;
        else {
          for (var g = !1, x = s.child; x; ) {
            if (x === i) {
              g = !0, i = s, o = f;
              break;
            }
            if (x === o) {
              g = !0, o = s, i = f;
              break;
            }
            x = x.sibling;
          }
          if (!g) {
            for (x = f.child; x; ) {
              if (x === i) {
                g = !0, i = f, o = s;
                break;
              }
              if (x === o) {
                g = !0, o = f, i = s;
                break;
              }
              x = x.sibling;
            }
            if (!g)
              throw new Error("Child was not found in either parent set. This indicates a bug in React related to the return pointer. Please file an issue.");
          }
        }
        if (i.alternate !== o)
          throw new Error("Return fibers should always be each others' alternates. This error is likely caused by a bug in React. Please file an issue.");
      }
      if (i.tag !== ne)
        throw new Error("Unable to find node on an unmounted component.");
      return i.stateNode.current === i ? e : t;
    }
    function Ba(e) {
      var t = vn(e);
      return t !== null ? Ld(t) : null;
    }
    function Ld(e) {
      if (e.tag === V || e.tag === $)
        return e;
      for (var t = e.child; t !== null; ) {
        var a = Ld(t);
        if (a !== null)
          return a;
        t = t.sibling;
      }
      return null;
    }
    function Yv(e) {
      var t = vn(e);
      return t !== null ? kc(t) : null;
    }
    function kc(e) {
      if (e.tag === V || e.tag === $)
        return e;
      for (var t = e.child; t !== null; ) {
        if (t.tag !== oe) {
          var a = kc(t);
          if (a !== null)
            return a;
        }
        t = t.sibling;
      }
      return null;
    }
    var _c = w.unstable_scheduleCallback, Wv = w.unstable_cancelCallback, Dc = w.unstable_shouldYield, Qv = w.unstable_requestPaint, wn = w.unstable_now, jd = w.unstable_getCurrentPriorityLevel, Nc = w.unstable_ImmediatePriority, so = w.unstable_UserBlockingPriority, Ri = w.unstable_NormalPriority, Gv = w.unstable_LowPriority, Oc = w.unstable_IdlePriority, lu = w.unstable_yieldValue, qv = w.unstable_setDisableYieldValue, qi = null, Qn = null, ve = null, $a = !1, Ra = typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ < "u";
    function zd(e) {
      if (typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ > "u")
        return !1;
      var t = __REACT_DEVTOOLS_GLOBAL_HOOK__;
      if (t.isDisabled)
        return !0;
      if (!t.supportsFiber)
        return y("The installed version of React DevTools is too old and will not work with the current version of React. Please update React DevTools. https://reactjs.org/link/react-devtools"), !0;
      try {
        ft && (e = Et({}, e, {
          getLaneLabelMap: Xi,
          injectProfilingHooks: Xv
        })), qi = t.inject(e), Qn = t;
      } catch (a) {
        y("React instrumentation encountered an error: %s.", a);
      }
      return !!t.checkDCE;
    }
    function Ad(e, t) {
      if (Qn && typeof Qn.onScheduleFiberRoot == "function")
        try {
          Qn.onScheduleFiberRoot(qi, e, t);
        } catch (a) {
          $a || ($a = !0, y("React instrumentation encountered an error: %s", a));
        }
    }
    function ou(e, t) {
      if (Qn && typeof Qn.onCommitFiberRoot == "function")
        try {
          var a = (e.current.flags & ot) === ot;
          if (vt) {
            var i;
            switch (t) {
              case zn:
                i = Nc;
                break;
              case Ji:
                i = so;
                break;
              case Ti:
                i = Ri;
                break;
              case Su:
                i = Oc;
                break;
              default:
                i = Ri;
                break;
            }
            Qn.onCommitFiberRoot(qi, e, i, a);
          }
        } catch (o) {
          $a || ($a = !0, y("React instrumentation encountered an error: %s", o));
        }
    }
    function Ia(e) {
      if (Qn && typeof Qn.onPostCommitFiberRoot == "function")
        try {
          Qn.onPostCommitFiberRoot(qi, e);
        } catch (t) {
          $a || ($a = !0, y("React instrumentation encountered an error: %s", t));
        }
    }
    function co(e) {
      if (Qn && typeof Qn.onCommitFiberUnmount == "function")
        try {
          Qn.onCommitFiberUnmount(qi, e);
        } catch (t) {
          $a || ($a = !0, y("React instrumentation encountered an error: %s", t));
        }
    }
    function Bn(e) {
      if (typeof lu == "function" && (qv(e), X(e)), Qn && typeof Qn.setStrictMode == "function")
        try {
          Qn.setStrictMode(qi, e);
        } catch (t) {
          $a || ($a = !0, y("React instrumentation encountered an error: %s", t));
        }
    }
    function Xv(e) {
      ve = e;
    }
    function Xi() {
      {
        for (var e = /* @__PURE__ */ new Map(), t = 1, a = 0; a < Es; a++) {
          var i = ky(t);
          e.set(t, i), t *= 2;
        }
        return e;
      }
    }
    function Ml(e) {
      ve !== null && typeof ve.markCommitStarted == "function" && ve.markCommitStarted(e);
    }
    function Mc() {
      ve !== null && typeof ve.markCommitStopped == "function" && ve.markCommitStopped();
    }
    function uu(e) {
      ve !== null && typeof ve.markComponentRenderStarted == "function" && ve.markComponentRenderStarted(e);
    }
    function oa() {
      ve !== null && typeof ve.markComponentRenderStopped == "function" && ve.markComponentRenderStopped();
    }
    function Ll(e) {
      ve !== null && typeof ve.markComponentPassiveEffectMountStarted == "function" && ve.markComponentPassiveEffectMountStarted(e);
    }
    function Lc() {
      ve !== null && typeof ve.markComponentPassiveEffectMountStopped == "function" && ve.markComponentPassiveEffectMountStopped();
    }
    function Kv(e) {
      ve !== null && typeof ve.markComponentPassiveEffectUnmountStarted == "function" && ve.markComponentPassiveEffectUnmountStarted(e);
    }
    function jc() {
      ve !== null && typeof ve.markComponentPassiveEffectUnmountStopped == "function" && ve.markComponentPassiveEffectUnmountStopped();
    }
    function Jv(e) {
      ve !== null && typeof ve.markComponentLayoutEffectMountStarted == "function" && ve.markComponentLayoutEffectMountStarted(e);
    }
    function Ss() {
      ve !== null && typeof ve.markComponentLayoutEffectMountStopped == "function" && ve.markComponentLayoutEffectMountStopped();
    }
    function di(e) {
      ve !== null && typeof ve.markComponentLayoutEffectUnmountStarted == "function" && ve.markComponentLayoutEffectUnmountStarted(e);
    }
    function su() {
      ve !== null && typeof ve.markComponentLayoutEffectUnmountStopped == "function" && ve.markComponentLayoutEffectUnmountStopped();
    }
    function xs(e, t, a) {
      ve !== null && typeof ve.markComponentErrored == "function" && ve.markComponentErrored(e, t, a);
    }
    function fo(e, t, a) {
      ve !== null && typeof ve.markComponentSuspended == "function" && ve.markComponentSuspended(e, t, a);
    }
    function Ud(e) {
      ve !== null && typeof ve.markLayoutEffectsStarted == "function" && ve.markLayoutEffectsStarted(e);
    }
    function cu() {
      ve !== null && typeof ve.markLayoutEffectsStopped == "function" && ve.markLayoutEffectsStopped();
    }
    function Zv(e) {
      ve !== null && typeof ve.markPassiveEffectsStarted == "function" && ve.markPassiveEffectsStarted(e);
    }
    function Fd() {
      ve !== null && typeof ve.markPassiveEffectsStopped == "function" && ve.markPassiveEffectsStopped();
    }
    function gn(e) {
      ve !== null && typeof ve.markRenderStarted == "function" && ve.markRenderStarted(e);
    }
    function zc() {
      ve !== null && typeof ve.markRenderYielded == "function" && ve.markRenderYielded();
    }
    function Ac() {
      ve !== null && typeof ve.markRenderStopped == "function" && ve.markRenderStopped();
    }
    function Hd(e) {
      ve !== null && typeof ve.markRenderScheduled == "function" && ve.markRenderScheduled(e);
    }
    function Uc(e, t) {
      ve !== null && typeof ve.markForceUpdateScheduled == "function" && ve.markForceUpdateScheduled(e, t);
    }
    function bs(e, t) {
      ve !== null && typeof ve.markStateUpdateScheduled == "function" && ve.markStateUpdateScheduled(e, t);
    }
    var Fe = (
      /*                         */
      0
    ), Ve = (
      /*                 */
      1
    ), ut = (
      /*                    */
      2
    ), _t = (
      /*               */
      8
    ), Ta = (
      /*              */
      16
    ), fu = Math.clz32 ? Math.clz32 : kr, Cs = Math.log, Ty = Math.LN2;
    function kr(e) {
      var t = e >>> 0;
      return t === 0 ? 32 : 31 - (Cs(t) / Ty | 0) | 0;
    }
    var Es = 31, Z = (
      /*                        */
      0
    ), $n = (
      /*                          */
      0
    ), Qe = (
      /*                        */
      1
    ), fr = (
      /*    */
      2
    ), ka = (
      /*             */
      4
    ), Ki = (
      /*            */
      8
    ), Ya = (
      /*                     */
      16
    ), du = (
      /*                */
      32
    ), po = (
      /*                       */
      4194240
    ), pu = (
      /*                        */
      64
    ), Fc = (
      /*                        */
      128
    ), Hc = (
      /*                        */
      256
    ), Pc = (
      /*                        */
      512
    ), Vc = (
      /*                        */
      1024
    ), Bc = (
      /*                        */
      2048
    ), vo = (
      /*                        */
      4096
    ), $c = (
      /*                        */
      8192
    ), vu = (
      /*                        */
      16384
    ), hu = (
      /*                       */
      32768
    ), Ic = (
      /*                       */
      65536
    ), ws = (
      /*                       */
      131072
    ), Yc = (
      /*                       */
      262144
    ), Wc = (
      /*                       */
      524288
    ), Qc = (
      /*                       */
      1048576
    ), Gc = (
      /*                       */
      2097152
    ), mu = (
      /*                            */
      130023424
    ), ho = (
      /*                             */
      4194304
    ), qc = (
      /*                             */
      8388608
    ), Xc = (
      /*                             */
      16777216
    ), Pd = (
      /*                             */
      33554432
    ), Kc = (
      /*                             */
      67108864
    ), eh = ho, Rs = (
      /*          */
      134217728
    ), Vd = (
      /*                          */
      268435455
    ), yu = (
      /*               */
      268435456
    ), jl = (
      /*                        */
      536870912
    ), _r = (
      /*                   */
      1073741824
    );
    function ky(e) {
      {
        if (e & Qe)
          return "Sync";
        if (e & fr)
          return "InputContinuousHydration";
        if (e & ka)
          return "InputContinuous";
        if (e & Ki)
          return "DefaultHydration";
        if (e & Ya)
          return "Default";
        if (e & du)
          return "TransitionHydration";
        if (e & po)
          return "Transition";
        if (e & mu)
          return "Retry";
        if (e & Rs)
          return "SelectiveHydration";
        if (e & yu)
          return "IdleHydration";
        if (e & jl)
          return "Idle";
        if (e & _r)
          return "Offscreen";
      }
    }
    var fn = -1, Jc = pu, ua = ho;
    function mo(e) {
      switch (jn(e)) {
        case Qe:
          return Qe;
        case fr:
          return fr;
        case ka:
          return ka;
        case Ki:
          return Ki;
        case Ya:
          return Ya;
        case du:
          return du;
        case pu:
        case Fc:
        case Hc:
        case Pc:
        case Vc:
        case Bc:
        case vo:
        case $c:
        case vu:
        case hu:
        case Ic:
        case ws:
        case Yc:
        case Wc:
        case Qc:
        case Gc:
          return e & po;
        case ho:
        case qc:
        case Xc:
        case Pd:
        case Kc:
          return e & mu;
        case Rs:
          return Rs;
        case yu:
          return yu;
        case jl:
          return jl;
        case _r:
          return _r;
        default:
          return y("Should have found matching lanes. This is a bug in React."), e;
      }
    }
    function yo(e, t) {
      var a = e.pendingLanes;
      if (a === Z)
        return Z;
      var i = Z, o = e.suspendedLanes, s = e.pingedLanes, f = a & Vd;
      if (f !== Z) {
        var p = f & ~o;
        if (p !== Z)
          i = mo(p);
        else {
          var v = f & s;
          v !== Z && (i = mo(v));
        }
      } else {
        var g = a & ~o;
        g !== Z ? i = mo(g) : s !== Z && (i = mo(s));
      }
      if (i === Z)
        return Z;
      if (t !== Z && t !== i && // If we already suspended with a delay, then interrupting is fine. Don't
      // bother waiting until the root is complete.
      (t & o) === Z) {
        var x = jn(i), N = jn(t);
        if (
          // Tests whether the next lane is equal or lower priority than the wip
          // one. This works because the bits decrease in priority as you go left.
          x >= N || // Default priority updates should not interrupt transition updates. The
          // only difference between default updates and transition updates is that
          // default updates do not support refresh transitions.
          x === Ya && (N & po) !== Z
        )
          return t;
      }
      (i & ka) !== Z && (i |= a & Ya);
      var _ = e.entangledLanes;
      if (_ !== Z)
        for (var A = e.entanglements, P = i & _; P > 0; ) {
          var Q = Al(P), ge = 1 << Q;
          i |= A[Q], P &= ~ge;
        }
      return i;
    }
    function th(e, t) {
      for (var a = e.eventTimes, i = fn; t > 0; ) {
        var o = Al(t), s = 1 << o, f = a[o];
        f > i && (i = f), t &= ~s;
      }
      return i;
    }
    function nh(e, t) {
      switch (e) {
        case Qe:
        case fr:
        case ka:
          return t + 250;
        case Ki:
        case Ya:
        case du:
        case pu:
        case Fc:
        case Hc:
        case Pc:
        case Vc:
        case Bc:
        case vo:
        case $c:
        case vu:
        case hu:
        case Ic:
        case ws:
        case Yc:
        case Wc:
        case Qc:
        case Gc:
          return t + 5e3;
        case ho:
        case qc:
        case Xc:
        case Pd:
        case Kc:
          return fn;
        case Rs:
        case yu:
        case jl:
        case _r:
          return fn;
        default:
          return y("Should have found matching lanes. This is a bug in React."), fn;
      }
    }
    function rh(e, t) {
      for (var a = e.pendingLanes, i = e.suspendedLanes, o = e.pingedLanes, s = e.expirationTimes, f = a; f > 0; ) {
        var p = Al(f), v = 1 << p, g = s[p];
        g === fn ? ((v & i) === Z || (v & o) !== Z) && (s[p] = nh(v, t)) : g <= t && (e.expiredLanes |= v), f &= ~v;
      }
    }
    function Bd(e) {
      return mo(e.pendingLanes);
    }
    function zl(e) {
      var t = e.pendingLanes & ~_r;
      return t !== Z ? t : t & _r ? _r : Z;
    }
    function $d(e) {
      return (e & Qe) !== Z;
    }
    function Ts(e) {
      return (e & Vd) !== Z;
    }
    function ah(e) {
      return (e & mu) === e;
    }
    function ih(e) {
      var t = Qe | ka | Ya;
      return (e & t) === Z;
    }
    function lh(e) {
      return (e & po) === e;
    }
    function ks(e, t) {
      var a = fr | ka | Ki | Ya;
      return (t & a) !== Z;
    }
    function oh(e, t) {
      return (t & e.expiredLanes) !== Z;
    }
    function Id(e) {
      return (e & po) !== Z;
    }
    function uh() {
      var e = Jc;
      return Jc <<= 1, (Jc & po) === Z && (Jc = pu), e;
    }
    function sa() {
      var e = ua;
      return ua <<= 1, (ua & mu) === Z && (ua = ho), e;
    }
    function jn(e) {
      return e & -e;
    }
    function gu(e) {
      return jn(e);
    }
    function Al(e) {
      return 31 - fu(e);
    }
    function Zc(e) {
      return Al(e);
    }
    function ca(e, t) {
      return (e & t) !== Z;
    }
    function go(e, t) {
      return (e & t) === t;
    }
    function gt(e, t) {
      return e | t;
    }
    function _s(e, t) {
      return e & ~t;
    }
    function ef(e, t) {
      return e & t;
    }
    function _y(e) {
      return e;
    }
    function sh(e, t) {
      return e !== $n && e < t ? e : t;
    }
    function Ds(e) {
      for (var t = [], a = 0; a < Es; a++)
        t.push(e);
      return t;
    }
    function So(e, t, a) {
      e.pendingLanes |= t, t !== jl && (e.suspendedLanes = Z, e.pingedLanes = Z);
      var i = e.eventTimes, o = Zc(t);
      i[o] = a;
    }
    function ch(e, t) {
      e.suspendedLanes |= t, e.pingedLanes &= ~t;
      for (var a = e.expirationTimes, i = t; i > 0; ) {
        var o = Al(i), s = 1 << o;
        a[o] = fn, i &= ~s;
      }
    }
    function tf(e, t, a) {
      e.pingedLanes |= e.suspendedLanes & t;
    }
    function nf(e, t) {
      var a = e.pendingLanes & ~t;
      e.pendingLanes = t, e.suspendedLanes = Z, e.pingedLanes = Z, e.expiredLanes &= t, e.mutableReadLanes &= t, e.entangledLanes &= t;
      for (var i = e.entanglements, o = e.eventTimes, s = e.expirationTimes, f = a; f > 0; ) {
        var p = Al(f), v = 1 << p;
        i[p] = Z, o[p] = fn, s[p] = fn, f &= ~v;
      }
    }
    function Yd(e, t) {
      for (var a = e.entangledLanes |= t, i = e.entanglements, o = a; o; ) {
        var s = Al(o), f = 1 << s;
        // Is this one of the newly entangled lanes?
        f & t | // Is this lane transitively entangled with the newly entangled lanes?
        i[s] & t && (i[s] |= t), o &= ~f;
      }
    }
    function fh(e, t) {
      var a = jn(t), i;
      switch (a) {
        case ka:
          i = fr;
          break;
        case Ya:
          i = Ki;
          break;
        case pu:
        case Fc:
        case Hc:
        case Pc:
        case Vc:
        case Bc:
        case vo:
        case $c:
        case vu:
        case hu:
        case Ic:
        case ws:
        case Yc:
        case Wc:
        case Qc:
        case Gc:
        case ho:
        case qc:
        case Xc:
        case Pd:
        case Kc:
          i = du;
          break;
        case jl:
          i = yu;
          break;
        default:
          i = $n;
          break;
      }
      return (i & (e.suspendedLanes | t)) !== $n ? $n : i;
    }
    function rf(e, t, a) {
      if (Ra)
        for (var i = e.pendingUpdatersLaneMap; a > 0; ) {
          var o = Zc(a), s = 1 << o, f = i[o];
          f.add(t), a &= ~s;
        }
    }
    function Wd(e, t) {
      if (Ra)
        for (var a = e.pendingUpdatersLaneMap, i = e.memoizedUpdaters; t > 0; ) {
          var o = Zc(t), s = 1 << o, f = a[o];
          f.size > 0 && (f.forEach(function(p) {
            var v = p.alternate;
            (v === null || !i.has(v)) && i.add(p);
          }), f.clear()), t &= ~s;
        }
    }
    function Ns(e, t) {
      return null;
    }
    var zn = Qe, Ji = ka, Ti = Ya, Su = jl, xu = $n;
    function Wa() {
      return xu;
    }
    function Dn(e) {
      xu = e;
    }
    function Dr(e, t) {
      var a = xu;
      try {
        return xu = e, t();
      } finally {
        xu = a;
      }
    }
    function Dy(e, t) {
      return e !== 0 && e < t ? e : t;
    }
    function Ny(e, t) {
      return e === 0 || e > t ? e : t;
    }
    function bu(e, t) {
      return e !== 0 && e < t;
    }
    function dr(e) {
      var t = jn(e);
      return bu(zn, t) ? bu(Ji, t) ? Ts(t) ? Ti : Su : Ji : zn;
    }
    function af(e) {
      var t = e.current.memoizedState;
      return t.isDehydrated;
    }
    var Te;
    function Cu(e) {
      Te = e;
    }
    function Qd(e) {
      Te(e);
    }
    var lf;
    function Oy(e) {
      lf = e;
    }
    var Eu;
    function of(e) {
      Eu = e;
    }
    var uf;
    function dh(e) {
      uf = e;
    }
    var Gd;
    function ph(e) {
      Gd = e;
    }
    var Os = !1, wu = [], Sn = null, ir = null, Fr = null, Ru = /* @__PURE__ */ new Map(), Tu = /* @__PURE__ */ new Map(), lr = [], vh = [
      "mousedown",
      "mouseup",
      "touchcancel",
      "touchend",
      "touchstart",
      "auxclick",
      "dblclick",
      "pointercancel",
      "pointerdown",
      "pointerup",
      "dragend",
      "dragstart",
      "drop",
      "compositionend",
      "compositionstart",
      "keydown",
      "keypress",
      "keyup",
      "input",
      "textInput",
      // Intentionally camelCase
      "copy",
      "cut",
      "paste",
      "click",
      "change",
      "contextmenu",
      "reset",
      "submit"
    ];
    function ki(e) {
      return vh.indexOf(e) > -1;
    }
    function My(e, t, a, i, o) {
      return {
        blockedOn: e,
        domEventName: t,
        eventSystemFlags: a,
        nativeEvent: o,
        targetContainers: [i]
      };
    }
    function qd(e, t) {
      switch (e) {
        case "focusin":
        case "focusout":
          Sn = null;
          break;
        case "dragenter":
        case "dragleave":
          ir = null;
          break;
        case "mouseover":
        case "mouseout":
          Fr = null;
          break;
        case "pointerover":
        case "pointerout": {
          var a = t.pointerId;
          Ru.delete(a);
          break;
        }
        case "gotpointercapture":
        case "lostpointercapture": {
          var i = t.pointerId;
          Tu.delete(i);
          break;
        }
      }
    }
    function ku(e, t, a, i, o, s) {
      if (e === null || e.nativeEvent !== s) {
        var f = My(t, a, i, o, s);
        if (t !== null) {
          var p = Au(t);
          p !== null && lf(p);
        }
        return f;
      }
      e.eventSystemFlags |= i;
      var v = e.targetContainers;
      return o !== null && v.indexOf(o) === -1 && v.push(o), e;
    }
    function hh(e, t, a, i, o) {
      switch (t) {
        case "focusin": {
          var s = o;
          return Sn = ku(Sn, e, t, a, i, s), !0;
        }
        case "dragenter": {
          var f = o;
          return ir = ku(ir, e, t, a, i, f), !0;
        }
        case "mouseover": {
          var p = o;
          return Fr = ku(Fr, e, t, a, i, p), !0;
        }
        case "pointerover": {
          var v = o, g = v.pointerId;
          return Ru.set(g, ku(Ru.get(g) || null, e, t, a, i, v)), !0;
        }
        case "gotpointercapture": {
          var x = o, N = x.pointerId;
          return Tu.set(N, ku(Tu.get(N) || null, e, t, a, i, x)), !0;
        }
      }
      return !1;
    }
    function Xd(e) {
      var t = $s(e.target);
      if (t !== null) {
        var a = Ea(t);
        if (a !== null) {
          var i = a.tag;
          if (i === ke) {
            var o = Od(a);
            if (o !== null) {
              e.blockedOn = o, Gd(e.priority, function() {
                Eu(a);
              });
              return;
            }
          } else if (i === ne) {
            var s = a.stateNode;
            if (af(s)) {
              e.blockedOn = Tc(a);
              return;
            }
          }
        }
      }
      e.blockedOn = null;
    }
    function Ly(e) {
      for (var t = uf(), a = {
        blockedOn: null,
        target: e,
        priority: t
      }, i = 0; i < lr.length && bu(t, lr[i].priority); i++)
        ;
      lr.splice(i, 0, a), i === 0 && Xd(a);
    }
    function xo(e) {
      if (e.blockedOn !== null)
        return !1;
      for (var t = e.targetContainers; t.length > 0; ) {
        var a = t[0], i = Nr(e.domEventName, e.eventSystemFlags, a, e.nativeEvent);
        if (i === null) {
          var o = e.nativeEvent, s = new o.constructor(o.type, o);
          fs(s), o.target.dispatchEvent(s), Cy();
        } else {
          var f = Au(i);
          return f !== null && lf(f), e.blockedOn = i, !1;
        }
        t.shift();
      }
      return !0;
    }
    function sf(e, t, a) {
      xo(e) && a.delete(t);
    }
    function Qa() {
      Os = !1, Sn !== null && xo(Sn) && (Sn = null), ir !== null && xo(ir) && (ir = null), Fr !== null && xo(Fr) && (Fr = null), Ru.forEach(sf), Tu.forEach(sf);
    }
    function Ot(e, t) {
      e.blockedOn === t && (e.blockedOn = null, Os || (Os = !0, w.unstable_scheduleCallback(w.unstable_NormalPriority, Qa)));
    }
    function Nn(e) {
      if (wu.length > 0) {
        Ot(wu[0], e);
        for (var t = 1; t < wu.length; t++) {
          var a = wu[t];
          a.blockedOn === e && (a.blockedOn = null);
        }
      }
      Sn !== null && Ot(Sn, e), ir !== null && Ot(ir, e), Fr !== null && Ot(Fr, e);
      var i = function(p) {
        return Ot(p, e);
      };
      Ru.forEach(i), Tu.forEach(i);
      for (var o = 0; o < lr.length; o++) {
        var s = lr[o];
        s.blockedOn === e && (s.blockedOn = null);
      }
      for (; lr.length > 0; ) {
        var f = lr[0];
        if (f.blockedOn !== null)
          break;
        Xd(f), f.blockedOn === null && lr.shift();
      }
    }
    var hn = b.ReactCurrentBatchConfig, Gn = !0;
    function fa(e) {
      Gn = !!e;
    }
    function _u() {
      return Gn;
    }
    function qn(e, t, a) {
      var i = cf(t), o;
      switch (i) {
        case zn:
          o = Ms;
          break;
        case Ji:
          o = bo;
          break;
        case Ti:
        default:
          o = Du;
          break;
      }
      return o.bind(null, t, a, e);
    }
    function Ms(e, t, a, i) {
      var o = Wa(), s = hn.transition;
      hn.transition = null;
      try {
        Dn(zn), Du(e, t, a, i);
      } finally {
        Dn(o), hn.transition = s;
      }
    }
    function bo(e, t, a, i) {
      var o = Wa(), s = hn.transition;
      hn.transition = null;
      try {
        Dn(Ji), Du(e, t, a, i);
      } finally {
        Dn(o), hn.transition = s;
      }
    }
    function Du(e, t, a, i) {
      Gn && Kd(e, t, a, i);
    }
    function Kd(e, t, a, i) {
      var o = Nr(e, t, a, i);
      if (o === null) {
        Xy(e, t, i, Ul, a), qd(e, i);
        return;
      }
      if (hh(o, e, t, a, i)) {
        i.stopPropagation();
        return;
      }
      if (qd(e, i), t & ro && ki(e)) {
        for (; o !== null; ) {
          var s = Au(o);
          s !== null && Qd(s);
          var f = Nr(e, t, a, i);
          if (f === null && Xy(e, t, i, Ul, a), f === o)
            break;
          o = f;
        }
        o !== null && i.stopPropagation();
        return;
      }
      Xy(e, t, i, null, a);
    }
    var Ul = null;
    function Nr(e, t, a, i) {
      Ul = null;
      var o = bc(i), s = $s(o);
      if (s !== null) {
        var f = Ea(s);
        if (f === null)
          s = null;
        else {
          var p = f.tag;
          if (p === ke) {
            var v = Od(f);
            if (v !== null)
              return v;
            s = null;
          } else if (p === ne) {
            var g = f.stateNode;
            if (af(g))
              return Tc(f);
            s = null;
          } else
            f !== s && (s = null);
        }
      }
      return Ul = s, null;
    }
    function cf(e) {
      switch (e) {
        case "cancel":
        case "click":
        case "close":
        case "contextmenu":
        case "copy":
        case "cut":
        case "auxclick":
        case "dblclick":
        case "dragend":
        case "dragstart":
        case "drop":
        case "focusin":
        case "focusout":
        case "input":
        case "invalid":
        case "keydown":
        case "keypress":
        case "keyup":
        case "mousedown":
        case "mouseup":
        case "paste":
        case "pause":
        case "play":
        case "pointercancel":
        case "pointerdown":
        case "pointerup":
        case "ratechange":
        case "reset":
        case "resize":
        case "seeked":
        case "submit":
        case "touchcancel":
        case "touchend":
        case "touchstart":
        case "volumechange":
        case "change":
        case "selectionchange":
        case "textInput":
        case "compositionstart":
        case "compositionend":
        case "compositionupdate":
        case "beforeblur":
        case "afterblur":
        case "beforeinput":
        case "blur":
        case "fullscreenchange":
        case "focus":
        case "hashchange":
        case "popstate":
        case "select":
        case "selectstart":
          return zn;
        case "drag":
        case "dragenter":
        case "dragexit":
        case "dragleave":
        case "dragover":
        case "mousemove":
        case "mouseout":
        case "mouseover":
        case "pointermove":
        case "pointerout":
        case "pointerover":
        case "scroll":
        case "toggle":
        case "touchmove":
        case "wheel":
        case "mouseenter":
        case "mouseleave":
        case "pointerenter":
        case "pointerleave":
          return Ji;
        case "message": {
          var t = jd();
          switch (t) {
            case Nc:
              return zn;
            case so:
              return Ji;
            case Ri:
            case Gv:
              return Ti;
            case Oc:
              return Su;
            default:
              return Ti;
          }
        }
        default:
          return Ti;
      }
    }
    function Nu(e, t, a) {
      return e.addEventListener(t, a, !1), a;
    }
    function Zi(e, t, a) {
      return e.addEventListener(t, a, !0), a;
    }
    function ff(e, t, a, i) {
      return e.addEventListener(t, a, {
        capture: !0,
        passive: i
      }), a;
    }
    function Jd(e, t, a, i) {
      return e.addEventListener(t, a, {
        passive: i
      }), a;
    }
    var Ga = null, Ou = null, qa = null;
    function df(e) {
      return Ga = e, Ou = js(), !0;
    }
    function Ls() {
      Ga = null, Ou = null, qa = null;
    }
    function pf() {
      if (qa)
        return qa;
      var e, t = Ou, a = t.length, i, o = js(), s = o.length;
      for (e = 0; e < a && t[e] === o[e]; e++)
        ;
      var f = a - e;
      for (i = 1; i <= f && t[a - i] === o[s - i]; i++)
        ;
      var p = i > 1 ? 1 - i : void 0;
      return qa = o.slice(e, p), qa;
    }
    function js() {
      return "value" in Ga ? Ga.value : Ga.textContent;
    }
    function Co(e) {
      var t, a = e.keyCode;
      return "charCode" in e ? (t = e.charCode, t === 0 && a === 13 && (t = 13)) : t = a, t === 10 && (t = 13), t >= 32 || t === 13 ? t : 0;
    }
    function or() {
      return !0;
    }
    function el() {
      return !1;
    }
    function Rn(e) {
      function t(a, i, o, s, f) {
        this._reactName = a, this._targetInst = o, this.type = i, this.nativeEvent = s, this.target = f, this.currentTarget = null;
        for (var p in e)
          if (e.hasOwnProperty(p)) {
            var v = e[p];
            v ? this[p] = v(s) : this[p] = s[p];
          }
        var g = s.defaultPrevented != null ? s.defaultPrevented : s.returnValue === !1;
        return g ? this.isDefaultPrevented = or : this.isDefaultPrevented = el, this.isPropagationStopped = el, this;
      }
      return Et(t.prototype, {
        preventDefault: function() {
          this.defaultPrevented = !0;
          var a = this.nativeEvent;
          a && (a.preventDefault ? a.preventDefault() : typeof a.returnValue != "unknown" && (a.returnValue = !1), this.isDefaultPrevented = or);
        },
        stopPropagation: function() {
          var a = this.nativeEvent;
          a && (a.stopPropagation ? a.stopPropagation() : typeof a.cancelBubble != "unknown" && (a.cancelBubble = !0), this.isPropagationStopped = or);
        },
        /**
         * We release all dispatched `SyntheticEvent`s after each event loop, adding
         * them back into the pool. This allows a way to hold onto a reference that
         * won't be added back into the pool.
         */
        persist: function() {
        },
        /**
         * Checks if this event should be released back into the pool.
         *
         * @return {boolean} True if this should not be released, false otherwise.
         */
        isPersistent: or
      }), t;
    }
    var Xn = {
      eventPhase: 0,
      bubbles: 0,
      cancelable: 0,
      timeStamp: function(e) {
        return e.timeStamp || Date.now();
      },
      defaultPrevented: 0,
      isTrusted: 0
    }, vf = Rn(Xn), Eo = Et({}, Xn, {
      view: 0,
      detail: 0
    }), Zd = Rn(Eo), ep, _i, Mu;
    function tp(e) {
      e !== Mu && (Mu && e.type === "mousemove" ? (ep = e.screenX - Mu.screenX, _i = e.screenY - Mu.screenY) : (ep = 0, _i = 0), Mu = e);
    }
    var Di = Et({}, Eo, {
      screenX: 0,
      screenY: 0,
      clientX: 0,
      clientY: 0,
      pageX: 0,
      pageY: 0,
      ctrlKey: 0,
      shiftKey: 0,
      altKey: 0,
      metaKey: 0,
      getModifierState: np,
      button: 0,
      buttons: 0,
      relatedTarget: function(e) {
        return e.relatedTarget === void 0 ? e.fromElement === e.srcElement ? e.toElement : e.fromElement : e.relatedTarget;
      },
      movementX: function(e) {
        return "movementX" in e ? e.movementX : (tp(e), ep);
      },
      movementY: function(e) {
        return "movementY" in e ? e.movementY : _i;
      }
    }), hf = Rn(Di), wo = Et({}, Di, {
      dataTransfer: 0
    }), mh = Rn(wo), yh = Et({}, Eo, {
      relatedTarget: 0
    }), zs = Rn(yh), mf = Et({}, Xn, {
      animationName: 0,
      elapsedTime: 0,
      pseudoElement: 0
    }), jy = Rn(mf), zy = Et({}, Xn, {
      clipboardData: function(e) {
        return "clipboardData" in e ? e.clipboardData : window.clipboardData;
      }
    }), gh = Rn(zy), Sh = Et({}, Xn, {
      data: 0
    }), Fl = Rn(Sh), Ay = Fl, Lu = {
      Esc: "Escape",
      Spacebar: " ",
      Left: "ArrowLeft",
      Up: "ArrowUp",
      Right: "ArrowRight",
      Down: "ArrowDown",
      Del: "Delete",
      Win: "OS",
      Menu: "ContextMenu",
      Apps: "ContextMenu",
      Scroll: "ScrollLock",
      MozPrintableKey: "Unidentified"
    }, xh = {
      8: "Backspace",
      9: "Tab",
      12: "Clear",
      13: "Enter",
      16: "Shift",
      17: "Control",
      18: "Alt",
      19: "Pause",
      20: "CapsLock",
      27: "Escape",
      32: " ",
      33: "PageUp",
      34: "PageDown",
      35: "End",
      36: "Home",
      37: "ArrowLeft",
      38: "ArrowUp",
      39: "ArrowRight",
      40: "ArrowDown",
      45: "Insert",
      46: "Delete",
      112: "F1",
      113: "F2",
      114: "F3",
      115: "F4",
      116: "F5",
      117: "F6",
      118: "F7",
      119: "F8",
      120: "F9",
      121: "F10",
      122: "F11",
      123: "F12",
      144: "NumLock",
      145: "ScrollLock",
      224: "Meta"
    };
    function On(e) {
      if (e.key) {
        var t = Lu[e.key] || e.key;
        if (t !== "Unidentified")
          return t;
      }
      if (e.type === "keypress") {
        var a = Co(e);
        return a === 13 ? "Enter" : String.fromCharCode(a);
      }
      return e.type === "keydown" || e.type === "keyup" ? xh[e.keyCode] || "Unidentified" : "";
    }
    var Uy = {
      Alt: "altKey",
      Control: "ctrlKey",
      Meta: "metaKey",
      Shift: "shiftKey"
    };
    function bh(e) {
      var t = this, a = t.nativeEvent;
      if (a.getModifierState)
        return a.getModifierState(e);
      var i = Uy[e];
      return i ? !!a[i] : !1;
    }
    function np(e) {
      return bh;
    }
    var Fy = Et({}, Eo, {
      key: On,
      code: 0,
      location: 0,
      ctrlKey: 0,
      shiftKey: 0,
      altKey: 0,
      metaKey: 0,
      repeat: 0,
      locale: 0,
      getModifierState: np,
      // Legacy Interface
      charCode: function(e) {
        return e.type === "keypress" ? Co(e) : 0;
      },
      keyCode: function(e) {
        return e.type === "keydown" || e.type === "keyup" ? e.keyCode : 0;
      },
      which: function(e) {
        return e.type === "keypress" ? Co(e) : e.type === "keydown" || e.type === "keyup" ? e.keyCode : 0;
      }
    }), Ch = Rn(Fy), Eh = Et({}, Di, {
      pointerId: 0,
      width: 0,
      height: 0,
      pressure: 0,
      tangentialPressure: 0,
      tiltX: 0,
      tiltY: 0,
      twist: 0,
      pointerType: 0,
      isPrimary: 0
    }), wh = Rn(Eh), Xa = Et({}, Eo, {
      touches: 0,
      targetTouches: 0,
      changedTouches: 0,
      altKey: 0,
      metaKey: 0,
      ctrlKey: 0,
      shiftKey: 0,
      getModifierState: np
    }), rp = Rn(Xa), Hy = Et({}, Xn, {
      propertyName: 0,
      elapsedTime: 0,
      pseudoElement: 0
    }), Hl = Rn(Hy), yf = Et({}, Di, {
      deltaX: function(e) {
        return "deltaX" in e ? e.deltaX : (
          // Fallback to `wheelDeltaX` for Webkit and normalize (right is positive).
          "wheelDeltaX" in e ? -e.wheelDeltaX : 0
        );
      },
      deltaY: function(e) {
        return "deltaY" in e ? e.deltaY : (
          // Fallback to `wheelDeltaY` for Webkit and normalize (down is positive).
          "wheelDeltaY" in e ? -e.wheelDeltaY : (
            // Fallback to `wheelDelta` for IE<9 and normalize (down is positive).
            "wheelDelta" in e ? -e.wheelDelta : 0
          )
        );
      },
      deltaZ: 0,
      // Browsers without "deltaMode" is reporting in raw wheel delta where one
      // notch on the scroll is always +/- 120, roughly equivalent to pixels.
      // A good approximation of DOM_DELTA_LINE (1) is 5% of viewport size or
      // ~40 pixels, for DOM_DELTA_SCREEN (2) it is 87.5% of viewport size.
      deltaMode: 0
    }), Ro = Rn(yf), gf = [9, 13, 27, 32], Sf = 229, As = xn && "CompositionEvent" in window, Us = null;
    xn && "documentMode" in document && (Us = document.documentMode);
    var ap = xn && "TextEvent" in window && !Us, Rh = xn && (!As || Us && Us > 8 && Us <= 11), ip = 32, lp = String.fromCharCode(ip);
    function xf() {
      Fn("onBeforeInput", ["compositionend", "keypress", "textInput", "paste"]), Fn("onCompositionEnd", ["compositionend", "focusout", "keydown", "keypress", "keyup", "mousedown"]), Fn("onCompositionStart", ["compositionstart", "focusout", "keydown", "keypress", "keyup", "mousedown"]), Fn("onCompositionUpdate", ["compositionupdate", "focusout", "keydown", "keypress", "keyup", "mousedown"]);
    }
    var Fs = !1;
    function Th(e) {
      return (e.ctrlKey || e.altKey || e.metaKey) && // ctrlKey && altKey is equivalent to AltGr, and is not a command.
      !(e.ctrlKey && e.altKey);
    }
    function op(e) {
      switch (e) {
        case "compositionstart":
          return "onCompositionStart";
        case "compositionend":
          return "onCompositionEnd";
        case "compositionupdate":
          return "onCompositionUpdate";
      }
    }
    function Py(e, t) {
      return e === "keydown" && t.keyCode === Sf;
    }
    function up(e, t) {
      switch (e) {
        case "keyup":
          return gf.indexOf(t.keyCode) !== -1;
        case "keydown":
          return t.keyCode !== Sf;
        case "keypress":
        case "mousedown":
        case "focusout":
          return !0;
        default:
          return !1;
      }
    }
    function bf(e) {
      var t = e.detail;
      return typeof t == "object" && "data" in t ? t.data : null;
    }
    function Hs(e) {
      return e.locale === "ko";
    }
    var Pl = !1;
    function Cf(e, t, a, i, o) {
      var s, f;
      if (As ? s = op(t) : Pl ? up(t, i) && (s = "onCompositionEnd") : Py(t, i) && (s = "onCompositionStart"), !s)
        return null;
      Rh && !Hs(i) && (!Pl && s === "onCompositionStart" ? Pl = df(o) : s === "onCompositionEnd" && Pl && (f = pf()));
      var p = Mh(a, s);
      if (p.length > 0) {
        var v = new Fl(s, t, null, i, o);
        if (e.push({
          event: v,
          listeners: p
        }), f)
          v.data = f;
        else {
          var g = bf(i);
          g !== null && (v.data = g);
        }
      }
    }
    function kh(e, t) {
      switch (e) {
        case "compositionend":
          return bf(t);
        case "keypress":
          var a = t.which;
          return a !== ip ? null : (Fs = !0, lp);
        case "textInput":
          var i = t.data;
          return i === lp && Fs ? null : i;
        default:
          return null;
      }
    }
    function Vy(e, t) {
      if (Pl) {
        if (e === "compositionend" || !As && up(e, t)) {
          var a = pf();
          return Ls(), Pl = !1, a;
        }
        return null;
      }
      switch (e) {
        case "paste":
          return null;
        case "keypress":
          if (!Th(t)) {
            if (t.char && t.char.length > 1)
              return t.char;
            if (t.which)
              return String.fromCharCode(t.which);
          }
          return null;
        case "compositionend":
          return Rh && !Hs(t) ? null : t.data;
        default:
          return null;
      }
    }
    function Ef(e, t, a, i, o) {
      var s;
      if (ap ? s = kh(t, i) : s = Vy(t, i), !s)
        return null;
      var f = Mh(a, "onBeforeInput");
      if (f.length > 0) {
        var p = new Ay("onBeforeInput", "beforeinput", null, i, o);
        e.push({
          event: p,
          listeners: f
        }), p.data = s;
      }
    }
    function By(e, t, a, i, o, s, f) {
      Cf(e, t, a, i, o), Ef(e, t, a, i, o);
    }
    var Ps = {
      color: !0,
      date: !0,
      datetime: !0,
      "datetime-local": !0,
      email: !0,
      month: !0,
      number: !0,
      password: !0,
      range: !0,
      search: !0,
      tel: !0,
      text: !0,
      time: !0,
      url: !0,
      week: !0
    };
    function _h(e) {
      var t = e && e.nodeName && e.nodeName.toLowerCase();
      return t === "input" ? !!Ps[e.type] : t === "textarea";
    }
    /**
     * Checks if an event is supported in the current execution environment.
     *
     * NOTE: This will not work correctly for non-generic events such as `change`,
     * `reset`, `load`, `error`, and `select`.
     *
     * Borrows from Modernizr.
     *
     * @param {string} eventNameSuffix Event name, e.g. "click".
     * @return {boolean} True if the event is supported.
     * @internal
     * @license Modernizr 3.0.0pre (Custom Build) | MIT
     */
    function wf(e) {
      if (!xn)
        return !1;
      var t = "on" + e, a = t in document;
      if (!a) {
        var i = document.createElement("div");
        i.setAttribute(t, "return;"), a = typeof i[t] == "function";
      }
      return a;
    }
    function n() {
      Fn("onChange", ["change", "click", "focusin", "focusout", "input", "keydown", "keyup", "selectionchange"]);
    }
    function r(e, t, a, i) {
      Cc(i);
      var o = Mh(t, "onChange");
      if (o.length > 0) {
        var s = new vf("onChange", "change", null, a, i);
        e.push({
          event: s,
          listeners: o
        });
      }
    }
    var l = null, u = null;
    function c(e) {
      var t = e.nodeName && e.nodeName.toLowerCase();
      return t === "select" || t === "input" && e.type === "file";
    }
    function d(e) {
      var t = [];
      r(t, u, e, bc(e)), Ed(m, t);
    }
    function m(e) {
      nx(e, 0);
    }
    function E(e) {
      var t = Nf(e);
      if (qo(t))
        return e;
    }
    function k(e, t) {
      if (e === "change")
        return t;
    }
    var H = !1;
    xn && (H = wf("input") && (!document.documentMode || document.documentMode > 9));
    function re(e, t) {
      l = e, u = t, l.attachEvent("onpropertychange", te);
    }
    function ae() {
      l && (l.detachEvent("onpropertychange", te), l = null, u = null);
    }
    function te(e) {
      e.propertyName === "value" && E(u) && d(e);
    }
    function Ce(e, t, a) {
      e === "focusin" ? (ae(), re(t, a)) : e === "focusout" && ae();
    }
    function _e(e, t) {
      if (e === "selectionchange" || e === "keyup" || e === "keydown")
        return E(u);
    }
    function Le(e) {
      var t = e.nodeName;
      return t && t.toLowerCase() === "input" && (e.type === "checkbox" || e.type === "radio");
    }
    function An(e, t) {
      if (e === "click")
        return E(t);
    }
    function M(e, t) {
      if (e === "input" || e === "change")
        return E(t);
    }
    function D(e) {
      var t = e._wrapperState;
      !t || !t.controlled || e.type !== "number" || Je(e, "number", e.value);
    }
    function z(e, t, a, i, o, s, f) {
      var p = a ? Nf(a) : window, v, g;
      if (c(p) ? v = k : _h(p) ? H ? v = M : (v = _e, g = Ce) : Le(p) && (v = An), v) {
        var x = v(t, a);
        if (x) {
          r(e, x, i, o);
          return;
        }
      }
      g && g(t, p, a), t === "focusout" && D(p);
    }
    function se() {
      Yn("onMouseEnter", ["mouseout", "mouseover"]), Yn("onMouseLeave", ["mouseout", "mouseover"]), Yn("onPointerEnter", ["pointerout", "pointerover"]), Yn("onPointerLeave", ["pointerout", "pointerover"]);
    }
    function He(e, t, a, i, o, s, f) {
      var p = t === "mouseover" || t === "pointerover", v = t === "mouseout" || t === "pointerout";
      if (p && !Vv(i)) {
        var g = i.relatedTarget || i.fromElement;
        if (g && ($s(g) || Cp(g)))
          return;
      }
      if (!(!v && !p)) {
        var x;
        if (o.window === o)
          x = o;
        else {
          var N = o.ownerDocument;
          N ? x = N.defaultView || N.parentWindow : x = window;
        }
        var _, A;
        if (v) {
          var P = i.relatedTarget || i.toElement;
          if (_ = a, A = P ? $s(P) : null, A !== null) {
            var Q = Ea(A);
            (A !== Q || A.tag !== V && A.tag !== $) && (A = null);
          }
        } else
          _ = null, A = a;
        if (_ !== A) {
          var ge = hf, Xe = "onMouseLeave", Be = "onMouseEnter", Ht = "mouse";
          (t === "pointerout" || t === "pointerover") && (ge = wh, Xe = "onPointerLeave", Be = "onPointerEnter", Ht = "pointer");
          var Mt = _ == null ? x : Nf(_), L = A == null ? x : Nf(A), G = new ge(Xe, Ht + "leave", _, i, o);
          G.target = Mt, G.relatedTarget = L;
          var j = null, le = $s(o);
          if (le === a) {
            var we = new ge(Be, Ht + "enter", A, i, o);
            we.target = L, we.relatedTarget = Mt, j = we;
          }
          E1(e, G, j, _, A);
        }
      }
    }
    function tt(e, t) {
      return e === t && (e !== 0 || 1 / e === 1 / t) || e !== e && t !== t;
    }
    var De = typeof Object.is == "function" ? Object.is : tt;
    function nt(e, t) {
      if (De(e, t))
        return !0;
      if (typeof e != "object" || e === null || typeof t != "object" || t === null)
        return !1;
      var a = Object.keys(e), i = Object.keys(t);
      if (a.length !== i.length)
        return !1;
      for (var o = 0; o < a.length; o++) {
        var s = a[o];
        if (!Zn.call(t, s) || !De(e[s], t[s]))
          return !1;
      }
      return !0;
    }
    function Kn(e) {
      for (; e && e.firstChild; )
        e = e.firstChild;
      return e;
    }
    function $t(e) {
      for (; e; ) {
        if (e.nextSibling)
          return e.nextSibling;
        e = e.parentNode;
      }
    }
    function tl(e, t) {
      for (var a = Kn(e), i = 0, o = 0; a; ) {
        if (a.nodeType === $i) {
          if (o = i + a.textContent.length, i <= t && o >= t)
            return {
              node: a,
              offset: t - i
            };
          i = o;
        }
        a = Kn($t(a));
      }
    }
    function $y(e) {
      var t = e.ownerDocument, a = t && t.defaultView || window, i = a.getSelection && a.getSelection();
      if (!i || i.rangeCount === 0)
        return null;
      var o = i.anchorNode, s = i.anchorOffset, f = i.focusNode, p = i.focusOffset;
      try {
        o.nodeType, f.nodeType;
      } catch {
        return null;
      }
      return r1(e, o, s, f, p);
    }
    function r1(e, t, a, i, o) {
      var s = 0, f = -1, p = -1, v = 0, g = 0, x = e, N = null;
      e:
        for (; ; ) {
          for (var _ = null; x === t && (a === 0 || x.nodeType === $i) && (f = s + a), x === i && (o === 0 || x.nodeType === $i) && (p = s + o), x.nodeType === $i && (s += x.nodeValue.length), (_ = x.firstChild) !== null; )
            N = x, x = _;
          for (; ; ) {
            if (x === e)
              break e;
            if (N === t && ++v === a && (f = s), N === i && ++g === o && (p = s), (_ = x.nextSibling) !== null)
              break;
            x = N, N = x.parentNode;
          }
          x = _;
        }
      return f === -1 || p === -1 ? null : {
        start: f,
        end: p
      };
    }
    function a1(e, t) {
      var a = e.ownerDocument || document, i = a && a.defaultView || window;
      if (i.getSelection) {
        var o = i.getSelection(), s = e.textContent.length, f = Math.min(t.start, s), p = t.end === void 0 ? f : Math.min(t.end, s);
        if (!o.extend && f > p) {
          var v = p;
          p = f, f = v;
        }
        var g = tl(e, f), x = tl(e, p);
        if (g && x) {
          if (o.rangeCount === 1 && o.anchorNode === g.node && o.anchorOffset === g.offset && o.focusNode === x.node && o.focusOffset === x.offset)
            return;
          var N = a.createRange();
          N.setStart(g.node, g.offset), o.removeAllRanges(), f > p ? (o.addRange(N), o.extend(x.node, x.offset)) : (N.setEnd(x.node, x.offset), o.addRange(N));
        }
      }
    }
    function IS(e) {
      return e && e.nodeType === $i;
    }
    function YS(e, t) {
      return !e || !t ? !1 : e === t ? !0 : IS(e) ? !1 : IS(t) ? YS(e, t.parentNode) : "contains" in e ? e.contains(t) : e.compareDocumentPosition ? !!(e.compareDocumentPosition(t) & 16) : !1;
    }
    function i1(e) {
      return e && e.ownerDocument && YS(e.ownerDocument.documentElement, e);
    }
    function l1(e) {
      try {
        return typeof e.contentWindow.location.href == "string";
      } catch {
        return !1;
      }
    }
    function WS() {
      for (var e = window, t = wl(); t instanceof e.HTMLIFrameElement; ) {
        if (l1(t))
          e = t.contentWindow;
        else
          return t;
        t = wl(e.document);
      }
      return t;
    }
    function Iy(e) {
      var t = e && e.nodeName && e.nodeName.toLowerCase();
      return t && (t === "input" && (e.type === "text" || e.type === "search" || e.type === "tel" || e.type === "url" || e.type === "password") || t === "textarea" || e.contentEditable === "true");
    }
    function o1() {
      var e = WS();
      return {
        focusedElem: e,
        selectionRange: Iy(e) ? s1(e) : null
      };
    }
    function u1(e) {
      var t = WS(), a = e.focusedElem, i = e.selectionRange;
      if (t !== a && i1(a)) {
        i !== null && Iy(a) && c1(a, i);
        for (var o = [], s = a; s = s.parentNode; )
          s.nodeType === ta && o.push({
            element: s,
            left: s.scrollLeft,
            top: s.scrollTop
          });
        typeof a.focus == "function" && a.focus();
        for (var f = 0; f < o.length; f++) {
          var p = o[f];
          p.element.scrollLeft = p.left, p.element.scrollTop = p.top;
        }
      }
    }
    function s1(e) {
      var t;
      return "selectionStart" in e ? t = {
        start: e.selectionStart,
        end: e.selectionEnd
      } : t = $y(e), t || {
        start: 0,
        end: 0
      };
    }
    function c1(e, t) {
      var a = t.start, i = t.end;
      i === void 0 && (i = a), "selectionStart" in e ? (e.selectionStart = a, e.selectionEnd = Math.min(i, e.value.length)) : a1(e, t);
    }
    var f1 = xn && "documentMode" in document && document.documentMode <= 11;
    function d1() {
      Fn("onSelect", ["focusout", "contextmenu", "dragend", "focusin", "keydown", "keyup", "mousedown", "mouseup", "selectionchange"]);
    }
    var Rf = null, Yy = null, sp = null, Wy = !1;
    function p1(e) {
      if ("selectionStart" in e && Iy(e))
        return {
          start: e.selectionStart,
          end: e.selectionEnd
        };
      var t = e.ownerDocument && e.ownerDocument.defaultView || window, a = t.getSelection();
      return {
        anchorNode: a.anchorNode,
        anchorOffset: a.anchorOffset,
        focusNode: a.focusNode,
        focusOffset: a.focusOffset
      };
    }
    function v1(e) {
      return e.window === e ? e.document : e.nodeType === si ? e : e.ownerDocument;
    }
    function QS(e, t, a) {
      var i = v1(a);
      if (!(Wy || Rf == null || Rf !== wl(i))) {
        var o = p1(Rf);
        if (!sp || !nt(sp, o)) {
          sp = o;
          var s = Mh(Yy, "onSelect");
          if (s.length > 0) {
            var f = new vf("onSelect", "select", null, t, a);
            e.push({
              event: f,
              listeners: s
            }), f.target = Rf;
          }
        }
      }
    }
    function h1(e, t, a, i, o, s, f) {
      var p = a ? Nf(a) : window;
      switch (t) {
        case "focusin":
          (_h(p) || p.contentEditable === "true") && (Rf = p, Yy = a, sp = null);
          break;
        case "focusout":
          Rf = null, Yy = null, sp = null;
          break;
        case "mousedown":
          Wy = !0;
          break;
        case "contextmenu":
        case "mouseup":
        case "dragend":
          Wy = !1, QS(e, i, o);
          break;
        case "selectionchange":
          if (f1)
            break;
        case "keydown":
        case "keyup":
          QS(e, i, o);
      }
    }
    function Dh(e, t) {
      var a = {};
      return a[e.toLowerCase()] = t.toLowerCase(), a["Webkit" + e] = "webkit" + t, a["Moz" + e] = "moz" + t, a;
    }
    var Tf = {
      animationend: Dh("Animation", "AnimationEnd"),
      animationiteration: Dh("Animation", "AnimationIteration"),
      animationstart: Dh("Animation", "AnimationStart"),
      transitionend: Dh("Transition", "TransitionEnd")
    }, Qy = {}, GS = {};
    xn && (GS = document.createElement("div").style, "AnimationEvent" in window || (delete Tf.animationend.animation, delete Tf.animationiteration.animation, delete Tf.animationstart.animation), "TransitionEvent" in window || delete Tf.transitionend.transition);
    function Nh(e) {
      if (Qy[e])
        return Qy[e];
      if (!Tf[e])
        return e;
      var t = Tf[e];
      for (var a in t)
        if (t.hasOwnProperty(a) && a in GS)
          return Qy[e] = t[a];
      return e;
    }
    var qS = Nh("animationend"), XS = Nh("animationiteration"), KS = Nh("animationstart"), JS = Nh("transitionend"), ZS = /* @__PURE__ */ new Map(), ex = ["abort", "auxClick", "cancel", "canPlay", "canPlayThrough", "click", "close", "contextMenu", "copy", "cut", "drag", "dragEnd", "dragEnter", "dragExit", "dragLeave", "dragOver", "dragStart", "drop", "durationChange", "emptied", "encrypted", "ended", "error", "gotPointerCapture", "input", "invalid", "keyDown", "keyPress", "keyUp", "load", "loadedData", "loadedMetadata", "loadStart", "lostPointerCapture", "mouseDown", "mouseMove", "mouseOut", "mouseOver", "mouseUp", "paste", "pause", "play", "playing", "pointerCancel", "pointerDown", "pointerMove", "pointerOut", "pointerOver", "pointerUp", "progress", "rateChange", "reset", "resize", "seeked", "seeking", "stalled", "submit", "suspend", "timeUpdate", "touchCancel", "touchEnd", "touchStart", "volumeChange", "scroll", "toggle", "touchMove", "waiting", "wheel"];
    function ju(e, t) {
      ZS.set(e, t), Fn(t, [e]);
    }
    function m1() {
      for (var e = 0; e < ex.length; e++) {
        var t = ex[e], a = t.toLowerCase(), i = t[0].toUpperCase() + t.slice(1);
        ju(a, "on" + i);
      }
      ju(qS, "onAnimationEnd"), ju(XS, "onAnimationIteration"), ju(KS, "onAnimationStart"), ju("dblclick", "onDoubleClick"), ju("focusin", "onFocus"), ju("focusout", "onBlur"), ju(JS, "onTransitionEnd");
    }
    function y1(e, t, a, i, o, s, f) {
      var p = ZS.get(t);
      if (p !== void 0) {
        var v = vf, g = t;
        switch (t) {
          case "keypress":
            if (Co(i) === 0)
              return;
          case "keydown":
          case "keyup":
            v = Ch;
            break;
          case "focusin":
            g = "focus", v = zs;
            break;
          case "focusout":
            g = "blur", v = zs;
            break;
          case "beforeblur":
          case "afterblur":
            v = zs;
            break;
          case "click":
            if (i.button === 2)
              return;
          case "auxclick":
          case "dblclick":
          case "mousedown":
          case "mousemove":
          case "mouseup":
          case "mouseout":
          case "mouseover":
          case "contextmenu":
            v = hf;
            break;
          case "drag":
          case "dragend":
          case "dragenter":
          case "dragexit":
          case "dragleave":
          case "dragover":
          case "dragstart":
          case "drop":
            v = mh;
            break;
          case "touchcancel":
          case "touchend":
          case "touchmove":
          case "touchstart":
            v = rp;
            break;
          case qS:
          case XS:
          case KS:
            v = jy;
            break;
          case JS:
            v = Hl;
            break;
          case "scroll":
            v = Zd;
            break;
          case "wheel":
            v = Ro;
            break;
          case "copy":
          case "cut":
          case "paste":
            v = gh;
            break;
          case "gotpointercapture":
          case "lostpointercapture":
          case "pointercancel":
          case "pointerdown":
          case "pointermove":
          case "pointerout":
          case "pointerover":
          case "pointerup":
            v = wh;
            break;
        }
        var x = (s & ro) !== 0;
        {
          var N = !x && // TODO: ideally, we'd eventually add all events from
          // nonDelegatedEvents list in DOMPluginEventSystem.
          // Then we can remove this special list.
          // This is a breaking change that can wait until React 18.
          t === "scroll", _ = b1(a, p, i.type, x, N);
          if (_.length > 0) {
            var A = new v(p, g, null, i, o);
            e.push({
              event: A,
              listeners: _
            });
          }
        }
      }
    }
    m1(), se(), n(), d1(), xf();
    function g1(e, t, a, i, o, s, f) {
      y1(e, t, a, i, o, s);
      var p = (s & by) === 0;
      p && (He(e, t, a, i, o), z(e, t, a, i, o), h1(e, t, a, i, o), By(e, t, a, i, o));
    }
    var cp = ["abort", "canplay", "canplaythrough", "durationchange", "emptied", "encrypted", "ended", "error", "loadeddata", "loadedmetadata", "loadstart", "pause", "play", "playing", "progress", "ratechange", "resize", "seeked", "seeking", "stalled", "suspend", "timeupdate", "volumechange", "waiting"], Gy = new Set(["cancel", "close", "invalid", "load", "scroll", "toggle"].concat(cp));
    function tx(e, t, a) {
      var i = e.type || "unknown-event";
      e.currentTarget = a, Qi(i, t, void 0, e), e.currentTarget = null;
    }
    function S1(e, t, a) {
      var i;
      if (a)
        for (var o = t.length - 1; o >= 0; o--) {
          var s = t[o], f = s.instance, p = s.currentTarget, v = s.listener;
          if (f !== i && e.isPropagationStopped())
            return;
          tx(e, v, p), i = f;
        }
      else
        for (var g = 0; g < t.length; g++) {
          var x = t[g], N = x.instance, _ = x.currentTarget, A = x.listener;
          if (N !== i && e.isPropagationStopped())
            return;
          tx(e, A, _), i = N;
        }
    }
    function nx(e, t) {
      for (var a = (t & ro) !== 0, i = 0; i < e.length; i++) {
        var o = e[i], s = o.event, f = o.listeners;
        S1(s, f, a);
      }
      kd();
    }
    function x1(e, t, a, i, o) {
      var s = bc(a), f = [];
      g1(f, e, i, a, s, t), nx(f, t);
    }
    function Tn(e, t) {
      Gy.has(e) || y('Did not expect a listenToNonDelegatedEvent() call for "%s". This is a bug in React. Please file an issue.', e);
      var a = !1, i = Xw(t), o = w1(e, a);
      i.has(o) || (rx(t, e, ss, a), i.add(o));
    }
    function qy(e, t, a) {
      Gy.has(e) && !t && y('Did not expect a listenToNativeEvent() call for "%s" in the bubble phase. This is a bug in React. Please file an issue.', e);
      var i = 0;
      t && (i |= ro), rx(a, e, i, t);
    }
    var Oh = "_reactListening" + Math.random().toString(36).slice(2);
    function fp(e) {
      if (!e[Oh]) {
        e[Oh] = !0, St.forEach(function(a) {
          a !== "selectionchange" && (Gy.has(a) || qy(a, !1, e), qy(a, !0, e));
        });
        var t = e.nodeType === si ? e : e.ownerDocument;
        t !== null && (t[Oh] || (t[Oh] = !0, qy("selectionchange", !1, t)));
      }
    }
    function rx(e, t, a, i, o) {
      var s = qn(e, t, a), f = void 0;
      vs && (t === "touchstart" || t === "touchmove" || t === "wheel") && (f = !0), e = e, i ? f !== void 0 ? ff(e, t, s, f) : Zi(e, t, s) : f !== void 0 ? Jd(e, t, s, f) : Nu(e, t, s);
    }
    function ax(e, t) {
      return e === t || e.nodeType === Vn && e.parentNode === t;
    }
    function Xy(e, t, a, i, o) {
      var s = i;
      if (!(t & Yi) && !(t & ss)) {
        var f = o;
        if (i !== null) {
          var p = i;
          e:
            for (; ; ) {
              if (p === null)
                return;
              var v = p.tag;
              if (v === ne || v === oe) {
                var g = p.stateNode.containerInfo;
                if (ax(g, f))
                  break;
                if (v === oe)
                  for (var x = p.return; x !== null; ) {
                    var N = x.tag;
                    if (N === ne || N === oe) {
                      var _ = x.stateNode.containerInfo;
                      if (ax(_, f))
                        return;
                    }
                    x = x.return;
                  }
                for (; g !== null; ) {
                  var A = $s(g);
                  if (A === null)
                    return;
                  var P = A.tag;
                  if (P === V || P === $) {
                    p = s = A;
                    continue e;
                  }
                  g = g.parentNode;
                }
              }
              p = p.return;
            }
        }
      }
      Ed(function() {
        return x1(e, t, a, s);
      });
    }
    function dp(e, t, a) {
      return {
        instance: e,
        listener: t,
        currentTarget: a
      };
    }
    function b1(e, t, a, i, o, s) {
      for (var f = t !== null ? t + "Capture" : null, p = i ? f : t, v = [], g = e, x = null; g !== null; ) {
        var N = g, _ = N.stateNode, A = N.tag;
        if (A === V && _ !== null && (x = _, p !== null)) {
          var P = io(g, p);
          P != null && v.push(dp(g, P, x));
        }
        if (o)
          break;
        g = g.return;
      }
      return v;
    }
    function Mh(e, t) {
      for (var a = t + "Capture", i = [], o = e; o !== null; ) {
        var s = o, f = s.stateNode, p = s.tag;
        if (p === V && f !== null) {
          var v = f, g = io(o, a);
          g != null && i.unshift(dp(o, g, v));
          var x = io(o, t);
          x != null && i.push(dp(o, x, v));
        }
        o = o.return;
      }
      return i;
    }
    function kf(e) {
      if (e === null)
        return null;
      do
        e = e.return;
      while (e && e.tag !== V);
      return e || null;
    }
    function C1(e, t) {
      for (var a = e, i = t, o = 0, s = a; s; s = kf(s))
        o++;
      for (var f = 0, p = i; p; p = kf(p))
        f++;
      for (; o - f > 0; )
        a = kf(a), o--;
      for (; f - o > 0; )
        i = kf(i), f--;
      for (var v = o; v--; ) {
        if (a === i || i !== null && a === i.alternate)
          return a;
        a = kf(a), i = kf(i);
      }
      return null;
    }
    function ix(e, t, a, i, o) {
      for (var s = t._reactName, f = [], p = a; p !== null && p !== i; ) {
        var v = p, g = v.alternate, x = v.stateNode, N = v.tag;
        if (g !== null && g === i)
          break;
        if (N === V && x !== null) {
          var _ = x;
          if (o) {
            var A = io(p, s);
            A != null && f.unshift(dp(p, A, _));
          } else if (!o) {
            var P = io(p, s);
            P != null && f.push(dp(p, P, _));
          }
        }
        p = p.return;
      }
      f.length !== 0 && e.push({
        event: t,
        listeners: f
      });
    }
    function E1(e, t, a, i, o) {
      var s = i && o ? C1(i, o) : null;
      i !== null && ix(e, t, i, s, !1), o !== null && a !== null && ix(e, a, o, s, !0);
    }
    function w1(e, t) {
      return e + "__" + (t ? "capture" : "bubble");
    }
    var Ka = !1, pp = "dangerouslySetInnerHTML", Lh = "suppressContentEditableWarning", zu = "suppressHydrationWarning", lx = "autoFocus", Vs = "children", Bs = "style", jh = "__html", Ky, zh, vp, ox, Ah, ux, sx;
    Ky = {
      // There are working polyfills for <dialog>. Let people use it.
      dialog: !0,
      // Electron ships a custom <webview> tag to display external web content in
      // an isolated frame and process.
      // This tag is not present in non Electron environments such as JSDom which
      // is often used for testing purposes.
      // @see https://electronjs.org/docs/api/webview-tag
      webview: !0
    }, zh = function(e, t) {
      xc(e, t), gd(e, t), Pv(e, t, {
        registrationNameDependencies: ht,
        possibleRegistrationNames: Wt
      });
    }, ux = xn && !document.documentMode, vp = function(e, t, a) {
      if (!Ka) {
        var i = Uh(a), o = Uh(t);
        o !== i && (Ka = !0, y("Prop `%s` did not match. Server: %s Client: %s", e, JSON.stringify(o), JSON.stringify(i)));
      }
    }, ox = function(e) {
      if (!Ka) {
        Ka = !0;
        var t = [];
        e.forEach(function(a) {
          t.push(a);
        }), y("Extra attributes from the server: %s", t);
      }
    }, Ah = function(e, t) {
      t === !1 ? y("Expected `%s` listener to be a function, instead got `false`.\n\nIf you used to conditionally omit it with %s={condition && value}, pass %s={condition ? value : undefined} instead.", e, e, e) : y("Expected `%s` listener to be a function, instead got a value of `%s` type.", e, typeof t);
    }, sx = function(e, t) {
      var a = e.namespaceURI === Bi ? e.ownerDocument.createElement(e.tagName) : e.ownerDocument.createElementNS(e.namespaceURI, e.tagName);
      return a.innerHTML = t, a.innerHTML;
    };
    var R1 = /\r\n?/g, T1 = /\u0000|\uFFFD/g;
    function Uh(e) {
      Xr(e);
      var t = typeof e == "string" ? e : "" + e;
      return t.replace(R1, `
`).replace(T1, "");
    }
    function Fh(e, t, a, i) {
      var o = Uh(t), s = Uh(e);
      if (s !== o && (i && (Ka || (Ka = !0, y('Text content did not match. Server: "%s" Client: "%s"', s, o))), a && Se))
        throw new Error("Text content does not match server-rendered HTML.");
    }
    function cx(e) {
      return e.nodeType === si ? e : e.ownerDocument;
    }
    function k1() {
    }
    function Hh(e) {
      e.onclick = k1;
    }
    function _1(e, t, a, i, o) {
      for (var s in i)
        if (i.hasOwnProperty(s)) {
          var f = i[s];
          if (s === Bs)
            f && Object.freeze(f), Nv(t, f);
          else if (s === pp) {
            var p = f ? f[jh] : void 0;
            p != null && Sv(t, p);
          } else if (s === Vs)
            if (typeof f == "string") {
              var v = e !== "textarea" || f !== "";
              v && mc(t, f);
            } else
              typeof f == "number" && mc(t, "" + f);
          else
            s === Lh || s === zu || s === lx || (ht.hasOwnProperty(s) ? f != null && (typeof f != "function" && Ah(s, f), s === "onScroll" && Tn("scroll", t)) : f != null && xa(t, s, f, o));
        }
    }
    function D1(e, t, a, i) {
      for (var o = 0; o < t.length; o += 2) {
        var s = t[o], f = t[o + 1];
        s === Bs ? Nv(e, f) : s === pp ? Sv(e, f) : s === Vs ? mc(e, f) : xa(e, s, f, i);
      }
    }
    function N1(e, t, a, i) {
      var o, s = cx(a), f, p = i;
      if (p === Bi && (p = vc(e)), p === Bi) {
        if (o = Ii(e, t), !o && e !== e.toLowerCase() && y("<%s /> is using incorrect casing. Use PascalCase for React components, or lowercase for HTML elements.", e), e === "script") {
          var v = s.createElement("div");
          v.innerHTML = "<script><\/script>";
          var g = v.firstChild;
          f = v.removeChild(g);
        } else if (typeof t.is == "string")
          f = s.createElement(e, {
            is: t.is
          });
        else if (f = s.createElement(e), e === "select") {
          var x = f;
          t.multiple ? x.multiple = !0 : t.size && (x.size = t.size);
        }
      } else
        f = s.createElementNS(p, e);
      return p === Bi && !o && Object.prototype.toString.call(f) === "[object HTMLUnknownElement]" && !Zn.call(Ky, e) && (Ky[e] = !0, y("The tag <%s> is unrecognized in this browser. If you meant to render a React component, start its name with an uppercase letter.", e)), f;
    }
    function O1(e, t) {
      return cx(t).createTextNode(e);
    }
    function M1(e, t, a, i) {
      var o = Ii(t, a);
      zh(t, a);
      var s;
      switch (t) {
        case "dialog":
          Tn("cancel", e), Tn("close", e), s = a;
          break;
        case "iframe":
        case "object":
        case "embed":
          Tn("load", e), s = a;
          break;
        case "video":
        case "audio":
          for (var f = 0; f < cp.length; f++)
            Tn(cp[f], e);
          s = a;
          break;
        case "source":
          Tn("error", e), s = a;
          break;
        case "img":
        case "image":
        case "link":
          Tn("error", e), Tn("load", e), s = a;
          break;
        case "details":
          Tn("toggle", e), s = a;
          break;
        case "input":
          R(e, a), s = h(e, a), Tn("invalid", e);
          break;
        case "option":
          nn(e, a), s = a;
          break;
        case "select":
          is(e, a), s = as(e, a), Tn("invalid", e);
          break;
        case "textarea":
          mv(e, a), s = sd(e, a), Tn("invalid", e);
          break;
        default:
          s = a;
      }
      switch (gc(t, s), _1(t, e, i, s, o), t) {
        case "input":
          Aa(e), ue(e, a, !1);
          break;
        case "textarea":
          Aa(e), gv(e);
          break;
        case "option":
          un(e, a);
          break;
        case "select":
          od(e, a);
          break;
        default:
          typeof s.onClick == "function" && Hh(e);
          break;
      }
    }
    function L1(e, t, a, i, o) {
      zh(t, i);
      var s = null, f, p;
      switch (t) {
        case "input":
          f = h(e, a), p = h(e, i), s = [];
          break;
        case "select":
          f = as(e, a), p = as(e, i), s = [];
          break;
        case "textarea":
          f = sd(e, a), p = sd(e, i), s = [];
          break;
        default:
          f = a, p = i, typeof f.onClick != "function" && typeof p.onClick == "function" && Hh(e);
          break;
      }
      gc(t, p);
      var v, g, x = null;
      for (v in f)
        if (!(p.hasOwnProperty(v) || !f.hasOwnProperty(v) || f[v] == null))
          if (v === Bs) {
            var N = f[v];
            for (g in N)
              N.hasOwnProperty(g) && (x || (x = {}), x[g] = "");
          } else
            v === pp || v === Vs || v === Lh || v === zu || v === lx || (ht.hasOwnProperty(v) ? s || (s = []) : (s = s || []).push(v, null));
      for (v in p) {
        var _ = p[v], A = f != null ? f[v] : void 0;
        if (!(!p.hasOwnProperty(v) || _ === A || _ == null && A == null))
          if (v === Bs)
            if (_ && Object.freeze(_), A) {
              for (g in A)
                A.hasOwnProperty(g) && (!_ || !_.hasOwnProperty(g)) && (x || (x = {}), x[g] = "");
              for (g in _)
                _.hasOwnProperty(g) && A[g] !== _[g] && (x || (x = {}), x[g] = _[g]);
            } else
              x || (s || (s = []), s.push(v, x)), x = _;
          else if (v === pp) {
            var P = _ ? _[jh] : void 0, Q = A ? A[jh] : void 0;
            P != null && Q !== P && (s = s || []).push(v, P);
          } else
            v === Vs ? (typeof _ == "string" || typeof _ == "number") && (s = s || []).push(v, "" + _) : v === Lh || v === zu || (ht.hasOwnProperty(v) ? (_ != null && (typeof _ != "function" && Ah(v, _), v === "onScroll" && Tn("scroll", e)), !s && A !== _ && (s = [])) : (s = s || []).push(v, _));
      }
      return x && (os(x, p[Bs]), (s = s || []).push(Bs, x)), s;
    }
    function j1(e, t, a, i, o) {
      a === "input" && o.type === "radio" && o.name != null && F(e, o);
      var s = Ii(a, i), f = Ii(a, o);
      switch (D1(e, t, s, f), a) {
        case "input":
          Y(e, o);
          break;
        case "textarea":
          yv(e, o);
          break;
        case "select":
          fy(e, o);
          break;
      }
    }
    function z1(e) {
      {
        var t = e.toLowerCase();
        return Sc.hasOwnProperty(t) && Sc[t] || null;
      }
    }
    function A1(e, t, a, i, o, s, f) {
      var p, v;
      switch (p = Ii(t, a), zh(t, a), t) {
        case "dialog":
          Tn("cancel", e), Tn("close", e);
          break;
        case "iframe":
        case "object":
        case "embed":
          Tn("load", e);
          break;
        case "video":
        case "audio":
          for (var g = 0; g < cp.length; g++)
            Tn(cp[g], e);
          break;
        case "source":
          Tn("error", e);
          break;
        case "img":
        case "image":
        case "link":
          Tn("error", e), Tn("load", e);
          break;
        case "details":
          Tn("toggle", e);
          break;
        case "input":
          R(e, a), Tn("invalid", e);
          break;
        case "option":
          nn(e, a);
          break;
        case "select":
          is(e, a), Tn("invalid", e);
          break;
        case "textarea":
          mv(e, a), Tn("invalid", e);
          break;
      }
      gc(t, a);
      {
        v = /* @__PURE__ */ new Set();
        for (var x = e.attributes, N = 0; N < x.length; N++) {
          var _ = x[N].name.toLowerCase();
          switch (_) {
            case "value":
              break;
            case "checked":
              break;
            case "selected":
              break;
            default:
              v.add(x[N].name);
          }
        }
      }
      var A = null;
      for (var P in a)
        if (a.hasOwnProperty(P)) {
          var Q = a[P];
          if (P === Vs)
            typeof Q == "string" ? e.textContent !== Q && (a[zu] !== !0 && Fh(e.textContent, Q, s, f), A = [Vs, Q]) : typeof Q == "number" && e.textContent !== "" + Q && (a[zu] !== !0 && Fh(e.textContent, Q, s, f), A = [Vs, "" + Q]);
          else if (ht.hasOwnProperty(P))
            Q != null && (typeof Q != "function" && Ah(P, Q), P === "onScroll" && Tn("scroll", e));
          else if (f && // Convince Flow we've calculated it (it's DEV-only in this method.)
          typeof p == "boolean") {
            var ge = void 0, Xe = p && Re ? null : Mr(P);
            if (a[zu] !== !0) {
              if (!(P === Lh || P === zu || // Controlled attributes are not validated
              // TODO: Only ignore them on controlled tags.
              P === "value" || P === "checked" || P === "selected")) {
                if (P === pp) {
                  var Be = e.innerHTML, Ht = Q ? Q[jh] : void 0;
                  if (Ht != null) {
                    var Mt = sx(e, Ht);
                    Mt !== Be && vp(P, Be, Mt);
                  }
                } else if (P === Bs) {
                  if (v.delete(P), ux) {
                    var L = Sy(Q);
                    ge = e.getAttribute("style"), L !== ge && vp(P, ge, L);
                  }
                } else if (p && !Re)
                  v.delete(P.toLowerCase()), ge = yi(e, P, Q), Q !== ge && vp(P, ge, Q);
                else if (!Cn(P, Xe, p) && !tn(P, Q, Xe, p)) {
                  var G = !1;
                  if (Xe !== null)
                    v.delete(Xe.attributeName), ge = Sa(e, P, Q, Xe);
                  else {
                    var j = i;
                    if (j === Bi && (j = vc(t)), j === Bi)
                      v.delete(P.toLowerCase());
                    else {
                      var le = z1(P);
                      le !== null && le !== P && (G = !0, v.delete(le)), v.delete(P);
                    }
                    ge = yi(e, P, Q);
                  }
                  var we = Re;
                  !we && Q !== ge && !G && vp(P, ge, Q);
                }
              }
            }
          }
        }
      switch (f && // $FlowFixMe - Should be inferred as not undefined.
      v.size > 0 && a[zu] !== !0 && ox(v), t) {
        case "input":
          Aa(e), ue(e, a, !0);
          break;
        case "textarea":
          Aa(e), gv(e);
          break;
        case "select":
        case "option":
          break;
        default:
          typeof a.onClick == "function" && Hh(e);
          break;
      }
      return A;
    }
    function U1(e, t, a) {
      var i = e.nodeValue !== t;
      return i;
    }
    function Jy(e, t) {
      {
        if (Ka)
          return;
        Ka = !0, y("Did not expect server HTML to contain a <%s> in <%s>.", t.nodeName.toLowerCase(), e.nodeName.toLowerCase());
      }
    }
    function Zy(e, t) {
      {
        if (Ka)
          return;
        Ka = !0, y('Did not expect server HTML to contain the text node "%s" in <%s>.', t.nodeValue, e.nodeName.toLowerCase());
      }
    }
    function eg(e, t, a) {
      {
        if (Ka)
          return;
        Ka = !0, y("Expected server HTML to contain a matching <%s> in <%s>.", t, e.nodeName.toLowerCase());
      }
    }
    function tg(e, t) {
      {
        if (t === "" || Ka)
          return;
        Ka = !0, y('Expected server HTML to contain a matching text node for "%s" in <%s>.', t, e.nodeName.toLowerCase());
      }
    }
    function F1(e, t, a) {
      switch (t) {
        case "input":
          et(e, a);
          return;
        case "textarea":
          cd(e, a);
          return;
        case "select":
          dy(e, a);
          return;
      }
    }
    var hp = function() {
    }, mp = function() {
    };
    {
      var H1 = ["address", "applet", "area", "article", "aside", "base", "basefont", "bgsound", "blockquote", "body", "br", "button", "caption", "center", "col", "colgroup", "dd", "details", "dir", "div", "dl", "dt", "embed", "fieldset", "figcaption", "figure", "footer", "form", "frame", "frameset", "h1", "h2", "h3", "h4", "h5", "h6", "head", "header", "hgroup", "hr", "html", "iframe", "img", "input", "isindex", "li", "link", "listing", "main", "marquee", "menu", "menuitem", "meta", "nav", "noembed", "noframes", "noscript", "object", "ol", "p", "param", "plaintext", "pre", "script", "section", "select", "source", "style", "summary", "table", "tbody", "td", "template", "textarea", "tfoot", "th", "thead", "title", "tr", "track", "ul", "wbr", "xmp"], fx = [
        "applet",
        "caption",
        "html",
        "table",
        "td",
        "th",
        "marquee",
        "object",
        "template",
        // https://html.spec.whatwg.org/multipage/syntax.html#html-integration-point
        // TODO: Distinguish by namespace here -- for <title>, including it here
        // errs on the side of fewer warnings
        "foreignObject",
        "desc",
        "title"
      ], P1 = fx.concat(["button"]), V1 = ["dd", "dt", "li", "option", "optgroup", "p", "rp", "rt"], dx = {
        current: null,
        formTag: null,
        aTagInScope: null,
        buttonTagInScope: null,
        nobrTagInScope: null,
        pTagInButtonScope: null,
        listItemTagAutoclosing: null,
        dlItemTagAutoclosing: null
      };
      mp = function(e, t) {
        var a = Et({}, e || dx), i = {
          tag: t
        };
        return fx.indexOf(t) !== -1 && (a.aTagInScope = null, a.buttonTagInScope = null, a.nobrTagInScope = null), P1.indexOf(t) !== -1 && (a.pTagInButtonScope = null), H1.indexOf(t) !== -1 && t !== "address" && t !== "div" && t !== "p" && (a.listItemTagAutoclosing = null, a.dlItemTagAutoclosing = null), a.current = i, t === "form" && (a.formTag = i), t === "a" && (a.aTagInScope = i), t === "button" && (a.buttonTagInScope = i), t === "nobr" && (a.nobrTagInScope = i), t === "p" && (a.pTagInButtonScope = i), t === "li" && (a.listItemTagAutoclosing = i), (t === "dd" || t === "dt") && (a.dlItemTagAutoclosing = i), a;
      };
      var B1 = function(e, t) {
        switch (t) {
          case "select":
            return e === "option" || e === "optgroup" || e === "#text";
          case "optgroup":
            return e === "option" || e === "#text";
          case "option":
            return e === "#text";
          case "tr":
            return e === "th" || e === "td" || e === "style" || e === "script" || e === "template";
          case "tbody":
          case "thead":
          case "tfoot":
            return e === "tr" || e === "style" || e === "script" || e === "template";
          case "colgroup":
            return e === "col" || e === "template";
          case "table":
            return e === "caption" || e === "colgroup" || e === "tbody" || e === "tfoot" || e === "thead" || e === "style" || e === "script" || e === "template";
          case "head":
            return e === "base" || e === "basefont" || e === "bgsound" || e === "link" || e === "meta" || e === "title" || e === "noscript" || e === "noframes" || e === "style" || e === "script" || e === "template";
          case "html":
            return e === "head" || e === "body" || e === "frameset";
          case "frameset":
            return e === "frame";
          case "#document":
            return e === "html";
        }
        switch (e) {
          case "h1":
          case "h2":
          case "h3":
          case "h4":
          case "h5":
          case "h6":
            return t !== "h1" && t !== "h2" && t !== "h3" && t !== "h4" && t !== "h5" && t !== "h6";
          case "rp":
          case "rt":
            return V1.indexOf(t) === -1;
          case "body":
          case "caption":
          case "col":
          case "colgroup":
          case "frameset":
          case "frame":
          case "head":
          case "html":
          case "tbody":
          case "td":
          case "tfoot":
          case "th":
          case "thead":
          case "tr":
            return t == null;
        }
        return !0;
      }, $1 = function(e, t) {
        switch (e) {
          case "address":
          case "article":
          case "aside":
          case "blockquote":
          case "center":
          case "details":
          case "dialog":
          case "dir":
          case "div":
          case "dl":
          case "fieldset":
          case "figcaption":
          case "figure":
          case "footer":
          case "header":
          case "hgroup":
          case "main":
          case "menu":
          case "nav":
          case "ol":
          case "p":
          case "section":
          case "summary":
          case "ul":
          case "pre":
          case "listing":
          case "table":
          case "hr":
          case "xmp":
          case "h1":
          case "h2":
          case "h3":
          case "h4":
          case "h5":
          case "h6":
            return t.pTagInButtonScope;
          case "form":
            return t.formTag || t.pTagInButtonScope;
          case "li":
            return t.listItemTagAutoclosing;
          case "dd":
          case "dt":
            return t.dlItemTagAutoclosing;
          case "button":
            return t.buttonTagInScope;
          case "a":
            return t.aTagInScope;
          case "nobr":
            return t.nobrTagInScope;
        }
        return null;
      }, px = {};
      hp = function(e, t, a) {
        a = a || dx;
        var i = a.current, o = i && i.tag;
        t != null && (e != null && y("validateDOMNesting: when childText is passed, childTag should be null"), e = "#text");
        var s = B1(e, o) ? null : i, f = s ? null : $1(e, a), p = s || f;
        if (p) {
          var v = p.tag, g = !!s + "|" + e + "|" + v;
          if (!px[g]) {
            px[g] = !0;
            var x = e, N = "";
            if (e === "#text" ? /\S/.test(t) ? x = "Text nodes" : (x = "Whitespace text nodes", N = " Make sure you don't have any extra whitespace between tags on each line of your source code.") : x = "<" + e + ">", s) {
              var _ = "";
              v === "table" && e === "tr" && (_ += " Add a <tbody>, <thead> or <tfoot> to your code to match the DOM tree generated by the browser."), y("validateDOMNesting(...): %s cannot appear as a child of <%s>.%s%s", x, v, N, _);
            } else
              y("validateDOMNesting(...): %s cannot appear as a descendant of <%s>.", x, v);
          }
        }
      };
    }
    var Ph = "suppressHydrationWarning", Vh = "$", Bh = "/$", yp = "$?", gp = "$!", I1 = "style", ng = null, rg = null;
    function Y1(e) {
      var t, a, i = e.nodeType;
      switch (i) {
        case si:
        case to: {
          t = i === si ? "#document" : "#fragment";
          var o = e.documentElement;
          a = o ? o.namespaceURI : dd(null, "");
          break;
        }
        default: {
          var s = i === Vn ? e.parentNode : e, f = s.namespaceURI || null;
          t = s.tagName, a = dd(f, t);
          break;
        }
      }
      {
        var p = t.toLowerCase(), v = mp(null, p);
        return {
          namespace: a,
          ancestorInfo: v
        };
      }
    }
    function W1(e, t, a) {
      {
        var i = e, o = dd(i.namespace, t), s = mp(i.ancestorInfo, t);
        return {
          namespace: o,
          ancestorInfo: s
        };
      }
    }
    function bN(e) {
      return e;
    }
    function Q1(e) {
      ng = _u(), rg = o1();
      var t = null;
      return fa(!1), t;
    }
    function G1(e) {
      u1(rg), fa(ng), ng = null, rg = null;
    }
    function q1(e, t, a, i, o) {
      var s;
      {
        var f = i;
        if (hp(e, null, f.ancestorInfo), typeof t.children == "string" || typeof t.children == "number") {
          var p = "" + t.children, v = mp(f.ancestorInfo, e);
          hp(null, p, v);
        }
        s = f.namespace;
      }
      var g = N1(e, t, a, s);
      return bp(o, g), fg(g, t), g;
    }
    function X1(e, t) {
      e.appendChild(t);
    }
    function K1(e, t, a, i, o) {
      switch (M1(e, t, a, i), t) {
        case "button":
        case "input":
        case "select":
        case "textarea":
          return !!a.autoFocus;
        case "img":
          return !0;
        default:
          return !1;
      }
    }
    function J1(e, t, a, i, o, s) {
      {
        var f = s;
        if (typeof i.children != typeof a.children && (typeof i.children == "string" || typeof i.children == "number")) {
          var p = "" + i.children, v = mp(f.ancestorInfo, t);
          hp(null, p, v);
        }
      }
      return L1(e, t, a, i);
    }
    function ag(e, t) {
      return e === "textarea" || e === "noscript" || typeof t.children == "string" || typeof t.children == "number" || typeof t.dangerouslySetInnerHTML == "object" && t.dangerouslySetInnerHTML !== null && t.dangerouslySetInnerHTML.__html != null;
    }
    function Z1(e, t, a, i) {
      {
        var o = a;
        hp(null, e, o.ancestorInfo);
      }
      var s = O1(e, t);
      return bp(i, s), s;
    }
    function ew() {
      var e = window.event;
      return e === void 0 ? Ti : cf(e.type);
    }
    var ig = typeof setTimeout == "function" ? setTimeout : void 0, tw = typeof clearTimeout == "function" ? clearTimeout : void 0, lg = -1, vx = typeof Promise == "function" ? Promise : void 0, nw = typeof queueMicrotask == "function" ? queueMicrotask : typeof vx < "u" ? function(e) {
      return vx.resolve(null).then(e).catch(rw);
    } : ig;
    function rw(e) {
      setTimeout(function() {
        throw e;
      });
    }
    function aw(e, t, a, i) {
      switch (t) {
        case "button":
        case "input":
        case "select":
        case "textarea":
          a.autoFocus && e.focus();
          return;
        case "img": {
          a.src && (e.src = a.src);
          return;
        }
      }
    }
    function iw(e, t, a, i, o, s) {
      j1(e, t, a, i, o), fg(e, o);
    }
    function hx(e) {
      mc(e, "");
    }
    function lw(e, t, a) {
      e.nodeValue = a;
    }
    function ow(e, t) {
      e.appendChild(t);
    }
    function uw(e, t) {
      var a;
      e.nodeType === Vn ? (a = e.parentNode, a.insertBefore(t, e)) : (a = e, a.appendChild(t));
      var i = e._reactRootContainer;
      i == null && a.onclick === null && Hh(a);
    }
    function sw(e, t, a) {
      e.insertBefore(t, a);
    }
    function cw(e, t, a) {
      e.nodeType === Vn ? e.parentNode.insertBefore(t, a) : e.insertBefore(t, a);
    }
    function fw(e, t) {
      e.removeChild(t);
    }
    function dw(e, t) {
      e.nodeType === Vn ? e.parentNode.removeChild(t) : e.removeChild(t);
    }
    function og(e, t) {
      var a = t, i = 0;
      do {
        var o = a.nextSibling;
        if (e.removeChild(a), o && o.nodeType === Vn) {
          var s = o.data;
          if (s === Bh)
            if (i === 0) {
              e.removeChild(o), Nn(t);
              return;
            } else
              i--;
          else
            (s === Vh || s === yp || s === gp) && i++;
        }
        a = o;
      } while (a);
      Nn(t);
    }
    function pw(e, t) {
      e.nodeType === Vn ? og(e.parentNode, t) : e.nodeType === ta && og(e, t), Nn(e);
    }
    function vw(e) {
      e = e;
      var t = e.style;
      typeof t.setProperty == "function" ? t.setProperty("display", "none", "important") : t.display = "none";
    }
    function hw(e) {
      e.nodeValue = "";
    }
    function mw(e, t) {
      e = e;
      var a = t[I1], i = a != null && a.hasOwnProperty("display") ? a.display : null;
      e.style.display = yc("display", i);
    }
    function yw(e, t) {
      e.nodeValue = t;
    }
    function gw(e) {
      e.nodeType === ta ? e.textContent = "" : e.nodeType === si && e.documentElement && e.removeChild(e.documentElement);
    }
    function Sw(e, t, a) {
      return e.nodeType !== ta || t.toLowerCase() !== e.nodeName.toLowerCase() ? null : e;
    }
    function xw(e, t) {
      return t === "" || e.nodeType !== $i ? null : e;
    }
    function bw(e) {
      return e.nodeType !== Vn ? null : e;
    }
    function mx(e) {
      return e.data === yp;
    }
    function ug(e) {
      return e.data === gp;
    }
    function Cw(e) {
      var t = e.nextSibling && e.nextSibling.dataset, a, i, o;
      return t && (a = t.dgst, i = t.msg, o = t.stck), {
        message: i,
        digest: a,
        stack: o
      };
    }
    function Ew(e, t) {
      e._reactRetry = t;
    }
    function $h(e) {
      for (; e != null; e = e.nextSibling) {
        var t = e.nodeType;
        if (t === ta || t === $i)
          break;
        if (t === Vn) {
          var a = e.data;
          if (a === Vh || a === gp || a === yp)
            break;
          if (a === Bh)
            return null;
        }
      }
      return e;
    }
    function Sp(e) {
      return $h(e.nextSibling);
    }
    function ww(e) {
      return $h(e.firstChild);
    }
    function Rw(e) {
      return $h(e.firstChild);
    }
    function Tw(e) {
      return $h(e.nextSibling);
    }
    function kw(e, t, a, i, o, s, f) {
      bp(s, e), fg(e, a);
      var p;
      {
        var v = o;
        p = v.namespace;
      }
      var g = (s.mode & Ve) !== Fe;
      return A1(e, t, a, p, i, g, f);
    }
    function _w(e, t, a, i) {
      return bp(a, e), a.mode & Ve, U1(e, t);
    }
    function Dw(e, t) {
      bp(t, e);
    }
    function Nw(e) {
      for (var t = e.nextSibling, a = 0; t; ) {
        if (t.nodeType === Vn) {
          var i = t.data;
          if (i === Bh) {
            if (a === 0)
              return Sp(t);
            a--;
          } else
            (i === Vh || i === gp || i === yp) && a++;
        }
        t = t.nextSibling;
      }
      return null;
    }
    function yx(e) {
      for (var t = e.previousSibling, a = 0; t; ) {
        if (t.nodeType === Vn) {
          var i = t.data;
          if (i === Vh || i === gp || i === yp) {
            if (a === 0)
              return t;
            a--;
          } else
            i === Bh && a++;
        }
        t = t.previousSibling;
      }
      return null;
    }
    function Ow(e) {
      Nn(e);
    }
    function Mw(e) {
      Nn(e);
    }
    function Lw(e) {
      return e !== "head" && e !== "body";
    }
    function jw(e, t, a, i) {
      var o = !0;
      Fh(t.nodeValue, a, i, o);
    }
    function zw(e, t, a, i, o, s) {
      if (t[Ph] !== !0) {
        var f = !0;
        Fh(i.nodeValue, o, s, f);
      }
    }
    function Aw(e, t) {
      t.nodeType === ta ? Jy(e, t) : t.nodeType === Vn || Zy(e, t);
    }
    function Uw(e, t) {
      {
        var a = e.parentNode;
        a !== null && (t.nodeType === ta ? Jy(a, t) : t.nodeType === Vn || Zy(a, t));
      }
    }
    function Fw(e, t, a, i, o) {
      (o || t[Ph] !== !0) && (i.nodeType === ta ? Jy(a, i) : i.nodeType === Vn || Zy(a, i));
    }
    function Hw(e, t, a) {
      eg(e, t);
    }
    function Pw(e, t) {
      tg(e, t);
    }
    function Vw(e, t, a) {
      {
        var i = e.parentNode;
        i !== null && eg(i, t);
      }
    }
    function Bw(e, t) {
      {
        var a = e.parentNode;
        a !== null && tg(a, t);
      }
    }
    function $w(e, t, a, i, o, s) {
      (s || t[Ph] !== !0) && eg(a, i);
    }
    function Iw(e, t, a, i, o) {
      (o || t[Ph] !== !0) && tg(a, i);
    }
    function Yw(e) {
      y("An error occurred during hydration. The server HTML was replaced with client content in <%s>.", e.nodeName.toLowerCase());
    }
    function Ww(e) {
      fp(e);
    }
    var _f = Math.random().toString(36).slice(2), Df = "__reactFiber$" + _f, sg = "__reactProps$" + _f, xp = "__reactContainer$" + _f, cg = "__reactEvents$" + _f, Qw = "__reactListeners$" + _f, Gw = "__reactHandles$" + _f;
    function qw(e) {
      delete e[Df], delete e[sg], delete e[cg], delete e[Qw], delete e[Gw];
    }
    function bp(e, t) {
      t[Df] = e;
    }
    function Ih(e, t) {
      t[xp] = e;
    }
    function gx(e) {
      e[xp] = null;
    }
    function Cp(e) {
      return !!e[xp];
    }
    function $s(e) {
      var t = e[Df];
      if (t)
        return t;
      for (var a = e.parentNode; a; ) {
        if (t = a[xp] || a[Df], t) {
          var i = t.alternate;
          if (t.child !== null || i !== null && i.child !== null)
            for (var o = yx(e); o !== null; ) {
              var s = o[Df];
              if (s)
                return s;
              o = yx(o);
            }
          return t;
        }
        e = a, a = e.parentNode;
      }
      return null;
    }
    function Au(e) {
      var t = e[Df] || e[xp];
      return t && (t.tag === V || t.tag === $ || t.tag === ke || t.tag === ne) ? t : null;
    }
    function Nf(e) {
      if (e.tag === V || e.tag === $)
        return e.stateNode;
      throw new Error("getNodeFromInstance: Invalid argument.");
    }
    function Yh(e) {
      return e[sg] || null;
    }
    function fg(e, t) {
      e[sg] = t;
    }
    function Xw(e) {
      var t = e[cg];
      return t === void 0 && (t = e[cg] = /* @__PURE__ */ new Set()), t;
    }
    var Sx = {}, xx = b.ReactDebugCurrentFrame;
    function Wh(e) {
      if (e) {
        var t = e._owner, a = bi(e.type, e._source, t ? t.type : null);
        xx.setExtraStackFrame(a);
      } else
        xx.setExtraStackFrame(null);
    }
    function nl(e, t, a, i, o) {
      {
        var s = Function.call.bind(Zn);
        for (var f in e)
          if (s(e, f)) {
            var p = void 0;
            try {
              if (typeof e[f] != "function") {
                var v = Error((i || "React class") + ": " + a + " type `" + f + "` is invalid; it must be a function, usually from the `prop-types` package, but received `" + typeof e[f] + "`.This often happens because of typos such as `PropTypes.function` instead of `PropTypes.func`.");
                throw v.name = "Invariant Violation", v;
              }
              p = e[f](t, f, i, a, null, "SECRET_DO_NOT_PASS_THIS_OR_YOU_WILL_BE_FIRED");
            } catch (g) {
              p = g;
            }
            p && !(p instanceof Error) && (Wh(o), y("%s: type specification of %s `%s` is invalid; the type checker function must return `null` or an `Error` but returned a %s. You may have forgotten to pass an argument to the type checker creator (arrayOf, instanceOf, objectOf, oneOf, oneOfType, and shape all require an argument).", i || "React class", a, f, typeof p), Wh(null)), p instanceof Error && !(p.message in Sx) && (Sx[p.message] = !0, Wh(o), y("Failed %s type: %s", a, p.message), Wh(null));
          }
      }
    }
    var dg = [], Qh;
    Qh = [];
    var To = -1;
    function Uu(e) {
      return {
        current: e
      };
    }
    function da(e, t) {
      if (To < 0) {
        y("Unexpected pop.");
        return;
      }
      t !== Qh[To] && y("Unexpected Fiber popped."), e.current = dg[To], dg[To] = null, Qh[To] = null, To--;
    }
    function pa(e, t, a) {
      To++, dg[To] = e.current, Qh[To] = a, e.current = t;
    }
    var pg;
    pg = {};
    var pi = {};
    Object.freeze(pi);
    var ko = Uu(pi), Vl = Uu(!1), vg = pi;
    function Of(e, t, a) {
      return a && Bl(t) ? vg : ko.current;
    }
    function bx(e, t, a) {
      {
        var i = e.stateNode;
        i.__reactInternalMemoizedUnmaskedChildContext = t, i.__reactInternalMemoizedMaskedChildContext = a;
      }
    }
    function Mf(e, t) {
      {
        var a = e.type, i = a.contextTypes;
        if (!i)
          return pi;
        var o = e.stateNode;
        if (o && o.__reactInternalMemoizedUnmaskedChildContext === t)
          return o.__reactInternalMemoizedMaskedChildContext;
        var s = {};
        for (var f in i)
          s[f] = t[f];
        {
          var p = dt(e) || "Unknown";
          nl(i, s, "context", p);
        }
        return o && bx(e, t, s), s;
      }
    }
    function Gh() {
      return Vl.current;
    }
    function Bl(e) {
      {
        var t = e.childContextTypes;
        return t != null;
      }
    }
    function qh(e) {
      da(Vl, e), da(ko, e);
    }
    function hg(e) {
      da(Vl, e), da(ko, e);
    }
    function Cx(e, t, a) {
      {
        if (ko.current !== pi)
          throw new Error("Unexpected context found on stack. This error is likely caused by a bug in React. Please file an issue.");
        pa(ko, t, e), pa(Vl, a, e);
      }
    }
    function Ex(e, t, a) {
      {
        var i = e.stateNode, o = t.childContextTypes;
        if (typeof i.getChildContext != "function") {
          {
            var s = dt(e) || "Unknown";
            pg[s] || (pg[s] = !0, y("%s.childContextTypes is specified but there is no getChildContext() method on the instance. You can either define getChildContext() on %s or remove childContextTypes from it.", s, s));
          }
          return a;
        }
        var f = i.getChildContext();
        for (var p in f)
          if (!(p in o))
            throw new Error((dt(e) || "Unknown") + '.getChildContext(): key "' + p + '" is not defined in childContextTypes.');
        {
          var v = dt(e) || "Unknown";
          nl(o, f, "child context", v);
        }
        return Et({}, a, f);
      }
    }
    function Xh(e) {
      {
        var t = e.stateNode, a = t && t.__reactInternalMemoizedMergedChildContext || pi;
        return vg = ko.current, pa(ko, a, e), pa(Vl, Vl.current, e), !0;
      }
    }
    function wx(e, t, a) {
      {
        var i = e.stateNode;
        if (!i)
          throw new Error("Expected to have an instance by this point. This error is likely caused by a bug in React. Please file an issue.");
        if (a) {
          var o = Ex(e, t, vg);
          i.__reactInternalMemoizedMergedChildContext = o, da(Vl, e), da(ko, e), pa(ko, o, e), pa(Vl, a, e);
        } else
          da(Vl, e), pa(Vl, a, e);
      }
    }
    function Kw(e) {
      {
        if (!Md(e) || e.tag !== K)
          throw new Error("Expected subtree parent to be a mounted class component. This error is likely caused by a bug in React. Please file an issue.");
        var t = e;
        do {
          switch (t.tag) {
            case ne:
              return t.stateNode.context;
            case K: {
              var a = t.type;
              if (Bl(a))
                return t.stateNode.__reactInternalMemoizedMergedChildContext;
              break;
            }
          }
          t = t.return;
        } while (t !== null);
        throw new Error("Found unexpected detached subtree parent. This error is likely caused by a bug in React. Please file an issue.");
      }
    }
    var Fu = 0, Kh = 1, _o = null, mg = !1, yg = !1;
    function Rx(e) {
      _o === null ? _o = [e] : _o.push(e);
    }
    function Jw(e) {
      mg = !0, Rx(e);
    }
    function Tx() {
      mg && Hu();
    }
    function Hu() {
      if (!yg && _o !== null) {
        yg = !0;
        var e = 0, t = Wa();
        try {
          var a = !0, i = _o;
          for (Dn(zn); e < i.length; e++) {
            var o = i[e];
            do
              o = o(a);
            while (o !== null);
          }
          _o = null, mg = !1;
        } catch (s) {
          throw _o !== null && (_o = _o.slice(e + 1)), _c(Nc, Hu), s;
        } finally {
          Dn(t), yg = !1;
        }
      }
      return null;
    }
    var Lf = [], jf = 0, Jh = null, Zh = 0, Ni = [], Oi = 0, Is = null, Do = 1, No = "";
    function Zw(e) {
      return Ws(), (e.flags & Dd) !== qe;
    }
    function eR(e) {
      return Ws(), Zh;
    }
    function tR() {
      var e = No, t = Do, a = t & ~nR(t);
      return a.toString(32) + e;
    }
    function Ys(e, t) {
      Ws(), Lf[jf++] = Zh, Lf[jf++] = Jh, Jh = e, Zh = t;
    }
    function kx(e, t, a) {
      Ws(), Ni[Oi++] = Do, Ni[Oi++] = No, Ni[Oi++] = Is, Is = e;
      var i = Do, o = No, s = em(i) - 1, f = i & ~(1 << s), p = a + 1, v = em(t) + s;
      if (v > 30) {
        var g = s - s % 5, x = (1 << g) - 1, N = (f & x).toString(32), _ = f >> g, A = s - g, P = em(t) + A, Q = p << A, ge = Q | _, Xe = N + o;
        Do = 1 << P | ge, No = Xe;
      } else {
        var Be = p << s, Ht = Be | f, Mt = o;
        Do = 1 << v | Ht, No = Mt;
      }
    }
    function gg(e) {
      Ws();
      var t = e.return;
      if (t !== null) {
        var a = 1, i = 0;
        Ys(e, a), kx(e, a, i);
      }
    }
    function em(e) {
      return 32 - fu(e);
    }
    function nR(e) {
      return 1 << em(e) - 1;
    }
    function Sg(e) {
      for (; e === Jh; )
        Jh = Lf[--jf], Lf[jf] = null, Zh = Lf[--jf], Lf[jf] = null;
      for (; e === Is; )
        Is = Ni[--Oi], Ni[Oi] = null, No = Ni[--Oi], Ni[Oi] = null, Do = Ni[--Oi], Ni[Oi] = null;
    }
    function rR() {
      return Ws(), Is !== null ? {
        id: Do,
        overflow: No
      } : null;
    }
    function aR(e, t) {
      Ws(), Ni[Oi++] = Do, Ni[Oi++] = No, Ni[Oi++] = Is, Do = t.id, No = t.overflow, Is = e;
    }
    function Ws() {
      Pr() || y("Expected to be hydrating. This is a bug in React. Please file an issue.");
    }
    var Hr = null, Mi = null, rl = !1, Qs = !1, Pu = null;
    function iR() {
      rl && y("We should not be hydrating here. This is a bug in React. Please file a bug.");
    }
    function _x() {
      Qs = !0;
    }
    function lR() {
      return Qs;
    }
    function oR(e) {
      var t = e.stateNode.containerInfo;
      return Mi = Rw(t), Hr = e, rl = !0, Pu = null, Qs = !1, !0;
    }
    function uR(e, t, a) {
      return Mi = Tw(t), Hr = e, rl = !0, Pu = null, Qs = !1, a !== null && aR(e, a), !0;
    }
    function Dx(e, t) {
      switch (e.tag) {
        case ne: {
          Aw(e.stateNode.containerInfo, t);
          break;
        }
        case V: {
          var a = (e.mode & Ve) !== Fe;
          Fw(
            e.type,
            e.memoizedProps,
            e.stateNode,
            t,
            // TODO: Delete this argument when we remove the legacy root API.
            a
          );
          break;
        }
        case ke: {
          var i = e.memoizedState;
          i.dehydrated !== null && Uw(i.dehydrated, t);
          break;
        }
      }
    }
    function Nx(e, t) {
      Dx(e, t);
      var a = d_();
      a.stateNode = t, a.return = e;
      var i = e.deletions;
      i === null ? (e.deletions = [a], e.flags |= Gt) : i.push(a);
    }
    function xg(e, t) {
      {
        if (Qs)
          return;
        switch (e.tag) {
          case ne: {
            var a = e.stateNode.containerInfo;
            switch (t.tag) {
              case V:
                var i = t.type;
                t.pendingProps, Hw(a, i);
                break;
              case $:
                var o = t.pendingProps;
                Pw(a, o);
                break;
            }
            break;
          }
          case V: {
            var s = e.type, f = e.memoizedProps, p = e.stateNode;
            switch (t.tag) {
              case V: {
                var v = t.type, g = t.pendingProps, x = (e.mode & Ve) !== Fe;
                $w(
                  s,
                  f,
                  p,
                  v,
                  g,
                  // TODO: Delete this argument when we remove the legacy root API.
                  x
                );
                break;
              }
              case $: {
                var N = t.pendingProps, _ = (e.mode & Ve) !== Fe;
                Iw(
                  s,
                  f,
                  p,
                  N,
                  // TODO: Delete this argument when we remove the legacy root API.
                  _
                );
                break;
              }
            }
            break;
          }
          case ke: {
            var A = e.memoizedState, P = A.dehydrated;
            if (P !== null)
              switch (t.tag) {
                case V:
                  var Q = t.type;
                  t.pendingProps, Vw(P, Q);
                  break;
                case $:
                  var ge = t.pendingProps;
                  Bw(P, ge);
                  break;
              }
            break;
          }
          default:
            return;
        }
      }
    }
    function Ox(e, t) {
      t.flags = t.flags & ~Pa | pn, xg(e, t);
    }
    function Mx(e, t) {
      switch (e.tag) {
        case V: {
          var a = e.type;
          e.pendingProps;
          var i = Sw(t, a);
          return i !== null ? (e.stateNode = i, Hr = e, Mi = ww(i), !0) : !1;
        }
        case $: {
          var o = e.pendingProps, s = xw(t, o);
          return s !== null ? (e.stateNode = s, Hr = e, Mi = null, !0) : !1;
        }
        case ke: {
          var f = bw(t);
          if (f !== null) {
            var p = {
              dehydrated: f,
              treeContext: rR(),
              retryLane: _r
            };
            e.memoizedState = p;
            var v = p_(f);
            return v.return = e, e.child = v, Hr = e, Mi = null, !0;
          }
          return !1;
        }
        default:
          return !1;
      }
    }
    function bg(e) {
      return (e.mode & Ve) !== Fe && (e.flags & ot) === qe;
    }
    function Cg(e) {
      throw new Error("Hydration failed because the initial UI does not match what was rendered on the server.");
    }
    function Eg(e) {
      if (rl) {
        var t = Mi;
        if (!t) {
          bg(e) && (xg(Hr, e), Cg()), Ox(Hr, e), rl = !1, Hr = e;
          return;
        }
        var a = t;
        if (!Mx(e, t)) {
          bg(e) && (xg(Hr, e), Cg()), t = Sp(a);
          var i = Hr;
          if (!t || !Mx(e, t)) {
            Ox(Hr, e), rl = !1, Hr = e;
            return;
          }
          Nx(i, a);
        }
      }
    }
    function sR(e, t, a) {
      var i = e.stateNode, o = !Qs, s = kw(i, e.type, e.memoizedProps, t, a, e, o);
      return e.updateQueue = s, s !== null;
    }
    function cR(e) {
      var t = e.stateNode, a = e.memoizedProps, i = _w(t, a, e);
      if (i) {
        var o = Hr;
        if (o !== null)
          switch (o.tag) {
            case ne: {
              var s = o.stateNode.containerInfo, f = (o.mode & Ve) !== Fe;
              jw(
                s,
                t,
                a,
                // TODO: Delete this argument when we remove the legacy root API.
                f
              );
              break;
            }
            case V: {
              var p = o.type, v = o.memoizedProps, g = o.stateNode, x = (o.mode & Ve) !== Fe;
              zw(
                p,
                v,
                g,
                t,
                a,
                // TODO: Delete this argument when we remove the legacy root API.
                x
              );
              break;
            }
          }
      }
      return i;
    }
    function fR(e) {
      var t = e.memoizedState, a = t !== null ? t.dehydrated : null;
      if (!a)
        throw new Error("Expected to have a hydrated suspense instance. This error is likely caused by a bug in React. Please file an issue.");
      Dw(a, e);
    }
    function dR(e) {
      var t = e.memoizedState, a = t !== null ? t.dehydrated : null;
      if (!a)
        throw new Error("Expected to have a hydrated suspense instance. This error is likely caused by a bug in React. Please file an issue.");
      return Nw(a);
    }
    function Lx(e) {
      for (var t = e.return; t !== null && t.tag !== V && t.tag !== ne && t.tag !== ke; )
        t = t.return;
      Hr = t;
    }
    function tm(e) {
      if (e !== Hr)
        return !1;
      if (!rl)
        return Lx(e), rl = !0, !1;
      if (e.tag !== ne && (e.tag !== V || Lw(e.type) && !ag(e.type, e.memoizedProps))) {
        var t = Mi;
        if (t)
          if (bg(e))
            jx(e), Cg();
          else
            for (; t; )
              Nx(e, t), t = Sp(t);
      }
      return Lx(e), e.tag === ke ? Mi = dR(e) : Mi = Hr ? Sp(e.stateNode) : null, !0;
    }
    function pR() {
      return rl && Mi !== null;
    }
    function jx(e) {
      for (var t = Mi; t; )
        Dx(e, t), t = Sp(t);
    }
    function zf() {
      Hr = null, Mi = null, rl = !1, Qs = !1;
    }
    function zx() {
      Pu !== null && (_C(Pu), Pu = null);
    }
    function Pr() {
      return rl;
    }
    function wg(e) {
      Pu === null ? Pu = [e] : Pu.push(e);
    }
    var vR = b.ReactCurrentBatchConfig, hR = null;
    function mR() {
      return vR.transition;
    }
    var al = {
      recordUnsafeLifecycleWarnings: function(e, t) {
      },
      flushPendingUnsafeLifecycleWarnings: function() {
      },
      recordLegacyContextWarning: function(e, t) {
      },
      flushLegacyContextWarning: function() {
      },
      discardPendingWarnings: function() {
      }
    };
    {
      var yR = function(e) {
        for (var t = null, a = e; a !== null; )
          a.mode & _t && (t = a), a = a.return;
        return t;
      }, Gs = function(e) {
        var t = [];
        return e.forEach(function(a) {
          t.push(a);
        }), t.sort().join(", ");
      }, Ep = [], wp = [], Rp = [], Tp = [], kp = [], _p = [], qs = /* @__PURE__ */ new Set();
      al.recordUnsafeLifecycleWarnings = function(e, t) {
        qs.has(e.type) || (typeof t.componentWillMount == "function" && // Don't warn about react-lifecycles-compat polyfilled components.
        t.componentWillMount.__suppressDeprecationWarning !== !0 && Ep.push(e), e.mode & _t && typeof t.UNSAFE_componentWillMount == "function" && wp.push(e), typeof t.componentWillReceiveProps == "function" && t.componentWillReceiveProps.__suppressDeprecationWarning !== !0 && Rp.push(e), e.mode & _t && typeof t.UNSAFE_componentWillReceiveProps == "function" && Tp.push(e), typeof t.componentWillUpdate == "function" && t.componentWillUpdate.__suppressDeprecationWarning !== !0 && kp.push(e), e.mode & _t && typeof t.UNSAFE_componentWillUpdate == "function" && _p.push(e));
      }, al.flushPendingUnsafeLifecycleWarnings = function() {
        var e = /* @__PURE__ */ new Set();
        Ep.length > 0 && (Ep.forEach(function(_) {
          e.add(dt(_) || "Component"), qs.add(_.type);
        }), Ep = []);
        var t = /* @__PURE__ */ new Set();
        wp.length > 0 && (wp.forEach(function(_) {
          t.add(dt(_) || "Component"), qs.add(_.type);
        }), wp = []);
        var a = /* @__PURE__ */ new Set();
        Rp.length > 0 && (Rp.forEach(function(_) {
          a.add(dt(_) || "Component"), qs.add(_.type);
        }), Rp = []);
        var i = /* @__PURE__ */ new Set();
        Tp.length > 0 && (Tp.forEach(function(_) {
          i.add(dt(_) || "Component"), qs.add(_.type);
        }), Tp = []);
        var o = /* @__PURE__ */ new Set();
        kp.length > 0 && (kp.forEach(function(_) {
          o.add(dt(_) || "Component"), qs.add(_.type);
        }), kp = []);
        var s = /* @__PURE__ */ new Set();
        if (_p.length > 0 && (_p.forEach(function(_) {
          s.add(dt(_) || "Component"), qs.add(_.type);
        }), _p = []), t.size > 0) {
          var f = Gs(t);
          y(`Using UNSAFE_componentWillMount in strict mode is not recommended and may indicate bugs in your code. See https://reactjs.org/link/unsafe-component-lifecycles for details.

* Move code with side effects to componentDidMount, and set initial state in the constructor.

Please update the following components: %s`, f);
        }
        if (i.size > 0) {
          var p = Gs(i);
          y(`Using UNSAFE_componentWillReceiveProps in strict mode is not recommended and may indicate bugs in your code. See https://reactjs.org/link/unsafe-component-lifecycles for details.

* Move data fetching code or side effects to componentDidUpdate.
* If you're updating state whenever props change, refactor your code to use memoization techniques or move it to static getDerivedStateFromProps. Learn more at: https://reactjs.org/link/derived-state

Please update the following components: %s`, p);
        }
        if (s.size > 0) {
          var v = Gs(s);
          y(`Using UNSAFE_componentWillUpdate in strict mode is not recommended and may indicate bugs in your code. See https://reactjs.org/link/unsafe-component-lifecycles for details.

* Move data fetching code or side effects to componentDidUpdate.

Please update the following components: %s`, v);
        }
        if (e.size > 0) {
          var g = Gs(e);
          W(`componentWillMount has been renamed, and is not recommended for use. See https://reactjs.org/link/unsafe-component-lifecycles for details.

* Move code with side effects to componentDidMount, and set initial state in the constructor.
* Rename componentWillMount to UNSAFE_componentWillMount to suppress this warning in non-strict mode. In React 18.x, only the UNSAFE_ name will work. To rename all deprecated lifecycles to their new names, you can run \`npx react-codemod rename-unsafe-lifecycles\` in your project source folder.

Please update the following components: %s`, g);
        }
        if (a.size > 0) {
          var x = Gs(a);
          W(`componentWillReceiveProps has been renamed, and is not recommended for use. See https://reactjs.org/link/unsafe-component-lifecycles for details.

* Move data fetching code or side effects to componentDidUpdate.
* If you're updating state whenever props change, refactor your code to use memoization techniques or move it to static getDerivedStateFromProps. Learn more at: https://reactjs.org/link/derived-state
* Rename componentWillReceiveProps to UNSAFE_componentWillReceiveProps to suppress this warning in non-strict mode. In React 18.x, only the UNSAFE_ name will work. To rename all deprecated lifecycles to their new names, you can run \`npx react-codemod rename-unsafe-lifecycles\` in your project source folder.

Please update the following components: %s`, x);
        }
        if (o.size > 0) {
          var N = Gs(o);
          W(`componentWillUpdate has been renamed, and is not recommended for use. See https://reactjs.org/link/unsafe-component-lifecycles for details.

* Move data fetching code or side effects to componentDidUpdate.
* Rename componentWillUpdate to UNSAFE_componentWillUpdate to suppress this warning in non-strict mode. In React 18.x, only the UNSAFE_ name will work. To rename all deprecated lifecycles to their new names, you can run \`npx react-codemod rename-unsafe-lifecycles\` in your project source folder.

Please update the following components: %s`, N);
        }
      };
      var nm = /* @__PURE__ */ new Map(), Ax = /* @__PURE__ */ new Set();
      al.recordLegacyContextWarning = function(e, t) {
        var a = yR(e);
        if (a === null) {
          y("Expected to find a StrictMode component in a strict mode tree. This error is likely caused by a bug in React. Please file an issue.");
          return;
        }
        if (!Ax.has(e.type)) {
          var i = nm.get(a);
          (e.type.contextTypes != null || e.type.childContextTypes != null || t !== null && typeof t.getChildContext == "function") && (i === void 0 && (i = [], nm.set(a, i)), i.push(e));
        }
      }, al.flushLegacyContextWarning = function() {
        nm.forEach(function(e, t) {
          if (e.length !== 0) {
            var a = e[0], i = /* @__PURE__ */ new Set();
            e.forEach(function(s) {
              i.add(dt(s) || "Component"), Ax.add(s.type);
            });
            var o = Gs(i);
            try {
              Jt(a), y(`Legacy context API has been detected within a strict-mode tree.

The old API will be supported in all 16.x releases, but applications using it should migrate to the new version.

Please update the following components: %s

Learn more about this warning here: https://reactjs.org/link/legacy-context`, o);
            } finally {
              kn();
            }
          }
        });
      }, al.discardPendingWarnings = function() {
        Ep = [], wp = [], Rp = [], Tp = [], kp = [], _p = [], nm = /* @__PURE__ */ new Map();
      };
    }
    var Rg, Tg, kg, _g, Dg, Ux = function(e, t) {
    };
    Rg = !1, Tg = !1, kg = {}, _g = {}, Dg = {}, Ux = function(e, t) {
      if (!(e === null || typeof e != "object") && !(!e._store || e._store.validated || e.key != null)) {
        if (typeof e._store != "object")
          throw new Error("React Component in warnForMissingKey should have a _store. This error is likely caused by a bug in React. Please file an issue.");
        e._store.validated = !0;
        var a = dt(t) || "Component";
        _g[a] || (_g[a] = !0, y('Each child in a list should have a unique "key" prop. See https://reactjs.org/link/warning-keys for more information.'));
      }
    };
    function gR(e) {
      return e.prototype && e.prototype.isReactComponent;
    }
    function Dp(e, t, a) {
      var i = a.ref;
      if (i !== null && typeof i != "function" && typeof i != "object") {
        if ((e.mode & _t || Me) && // We warn in ReactElement.js if owner and self are equal for string refs
        // because these cannot be automatically converted to an arrow function
        // using a codemod. Therefore, we don't have to warn about string refs again.
        !(a._owner && a._self && a._owner.stateNode !== a._self) && // Will already throw with "Function components cannot have string refs"
        !(a._owner && a._owner.tag !== K) && // Will already warn with "Function components cannot be given refs"
        !(typeof a.type == "function" && !gR(a.type)) && // Will already throw with "Element ref was specified as a string (someStringRef) but no owner was set"
        a._owner) {
          var o = dt(e) || "Component";
          kg[o] || (y('Component "%s" contains the string ref "%s". Support for string refs will be removed in a future major release. We recommend using useRef() or createRef() instead. Learn more about using refs safely here: https://reactjs.org/link/strict-mode-string-ref', o, i), kg[o] = !0);
        }
        if (a._owner) {
          var s = a._owner, f;
          if (s) {
            var p = s;
            if (p.tag !== K)
              throw new Error("Function components cannot have string refs. We recommend using useRef() instead. Learn more about using refs safely here: https://reactjs.org/link/strict-mode-string-ref");
            f = p.stateNode;
          }
          if (!f)
            throw new Error("Missing owner for string ref " + i + ". This error is likely caused by a bug in React. Please file an issue.");
          var v = f;
          er(i, "ref");
          var g = "" + i;
          if (t !== null && t.ref !== null && typeof t.ref == "function" && t.ref._stringRef === g)
            return t.ref;
          var x = function(N) {
            var _ = v.refs;
            N === null ? delete _[g] : _[g] = N;
          };
          return x._stringRef = g, x;
        } else {
          if (typeof i != "string")
            throw new Error("Expected ref to be a function, a string, an object returned by React.createRef(), or null.");
          if (!a._owner)
            throw new Error("Element ref was specified as a string (" + i + `) but no owner was set. This could happen for one of the following reasons:
1. You may be adding a ref to a function component
2. You may be adding a ref to a component that was not created inside a component's render method
3. You have multiple copies of React loaded
See https://reactjs.org/link/refs-must-have-owner for more information.`);
        }
      }
      return i;
    }
    function rm(e, t) {
      var a = Object.prototype.toString.call(t);
      throw new Error("Objects are not valid as a React child (found: " + (a === "[object Object]" ? "object with keys {" + Object.keys(t).join(", ") + "}" : a) + "). If you meant to render a collection of children, use an array instead.");
    }
    function am(e) {
      {
        var t = dt(e) || "Component";
        if (Dg[t])
          return;
        Dg[t] = !0, y("Functions are not valid as a React child. This may happen if you return a Component instead of <Component /> from render. Or maybe you meant to call this function rather than return it.");
      }
    }
    function Fx(e) {
      var t = e._payload, a = e._init;
      return a(t);
    }
    function Hx(e) {
      function t(L, G) {
        if (e) {
          var j = L.deletions;
          j === null ? (L.deletions = [G], L.flags |= Gt) : j.push(G);
        }
      }
      function a(L, G) {
        if (!e)
          return null;
        for (var j = G; j !== null; )
          t(L, j), j = j.sibling;
        return null;
      }
      function i(L, G) {
        for (var j = /* @__PURE__ */ new Map(), le = G; le !== null; )
          le.key !== null ? j.set(le.key, le) : j.set(le.index, le), le = le.sibling;
        return j;
      }
      function o(L, G) {
        var j = ac(L, G);
        return j.index = 0, j.sibling = null, j;
      }
      function s(L, G, j) {
        if (L.index = j, !e)
          return L.flags |= Dd, G;
        var le = L.alternate;
        if (le !== null) {
          var we = le.index;
          return we < G ? (L.flags |= pn, G) : we;
        } else
          return L.flags |= pn, G;
      }
      function f(L) {
        return e && L.alternate === null && (L.flags |= pn), L;
      }
      function p(L, G, j, le) {
        if (G === null || G.tag !== $) {
          var we = wS(j, L.mode, le);
          return we.return = L, we;
        } else {
          var xe = o(G, j);
          return xe.return = L, xe;
        }
      }
      function v(L, G, j, le) {
        var we = j.type;
        if (we === ba)
          return x(L, G, j.props.children, le, j.key);
        if (G !== null && (G.elementType === we || // Keep this check inline so it only runs on the false path:
        IC(G, j) || // Lazy types should reconcile their resolved type.
        // We need to do this after the Hot Reloading check above,
        // because hot reloading has different semantics than prod because
        // it doesn't resuspend. So we can't let the call below suspend.
        typeof we == "object" && we !== null && we.$$typeof === Ze && Fx(we) === G.type)) {
          var xe = o(G, j.props);
          return xe.ref = Dp(L, G, j), xe.return = L, xe._debugSource = j._source, xe._debugOwner = j._owner, xe;
        }
        var lt = ES(j, L.mode, le);
        return lt.ref = Dp(L, G, j), lt.return = L, lt;
      }
      function g(L, G, j, le) {
        if (G === null || G.tag !== oe || G.stateNode.containerInfo !== j.containerInfo || G.stateNode.implementation !== j.implementation) {
          var we = RS(j, L.mode, le);
          return we.return = L, we;
        } else {
          var xe = o(G, j.children || []);
          return xe.return = L, xe;
        }
      }
      function x(L, G, j, le, we) {
        if (G === null || G.tag !== de) {
          var xe = Ku(j, L.mode, le, we);
          return xe.return = L, xe;
        } else {
          var lt = o(G, j);
          return lt.return = L, lt;
        }
      }
      function N(L, G, j) {
        if (typeof G == "string" && G !== "" || typeof G == "number") {
          var le = wS("" + G, L.mode, j);
          return le.return = L, le;
        }
        if (typeof G == "object" && G !== null) {
          switch (G.$$typeof) {
            case ii: {
              var we = ES(G, L.mode, j);
              return we.ref = Dp(L, null, G), we.return = L, we;
            }
            case Lr: {
              var xe = RS(G, L.mode, j);
              return xe.return = L, xe;
            }
            case Ze: {
              var lt = G._payload, mt = G._init;
              return N(L, mt(lt), j);
            }
          }
          if (At(G) || jr(G)) {
            var an = Ku(G, L.mode, j, null);
            return an.return = L, an;
          }
          rm(L, G);
        }
        return typeof G == "function" && am(L), null;
      }
      function _(L, G, j, le) {
        var we = G !== null ? G.key : null;
        if (typeof j == "string" && j !== "" || typeof j == "number")
          return we !== null ? null : p(L, G, "" + j, le);
        if (typeof j == "object" && j !== null) {
          switch (j.$$typeof) {
            case ii:
              return j.key === we ? v(L, G, j, le) : null;
            case Lr:
              return j.key === we ? g(L, G, j, le) : null;
            case Ze: {
              var xe = j._payload, lt = j._init;
              return _(L, G, lt(xe), le);
            }
          }
          if (At(j) || jr(j))
            return we !== null ? null : x(L, G, j, le, null);
          rm(L, j);
        }
        return typeof j == "function" && am(L), null;
      }
      function A(L, G, j, le, we) {
        if (typeof le == "string" && le !== "" || typeof le == "number") {
          var xe = L.get(j) || null;
          return p(G, xe, "" + le, we);
        }
        if (typeof le == "object" && le !== null) {
          switch (le.$$typeof) {
            case ii: {
              var lt = L.get(le.key === null ? j : le.key) || null;
              return v(G, lt, le, we);
            }
            case Lr: {
              var mt = L.get(le.key === null ? j : le.key) || null;
              return g(G, mt, le, we);
            }
            case Ze:
              var an = le._payload, It = le._init;
              return A(L, G, j, It(an), we);
          }
          if (At(le) || jr(le)) {
            var Jn = L.get(j) || null;
            return x(G, Jn, le, we, null);
          }
          rm(G, le);
        }
        return typeof le == "function" && am(G), null;
      }
      function P(L, G, j) {
        {
          if (typeof L != "object" || L === null)
            return G;
          switch (L.$$typeof) {
            case ii:
            case Lr:
              Ux(L, j);
              var le = L.key;
              if (typeof le != "string")
                break;
              if (G === null) {
                G = /* @__PURE__ */ new Set(), G.add(le);
                break;
              }
              if (!G.has(le)) {
                G.add(le);
                break;
              }
              y("Encountered two children with the same key, `%s`. Keys should be unique so that components maintain their identity across updates. Non-unique keys may cause children to be duplicated and/or omitted — the behavior is unsupported and could change in a future version.", le);
              break;
            case Ze:
              var we = L._payload, xe = L._init;
              P(xe(we), G, j);
              break;
          }
        }
        return G;
      }
      function Q(L, G, j, le) {
        for (var we = null, xe = 0; xe < j.length; xe++) {
          var lt = j[xe];
          we = P(lt, we, L);
        }
        for (var mt = null, an = null, It = G, Jn = 0, Yt = 0, In = null; It !== null && Yt < j.length; Yt++) {
          It.index > Yt ? (In = It, It = null) : In = It.sibling;
          var ha = _(L, It, j[Yt], le);
          if (ha === null) {
            It === null && (It = In);
            break;
          }
          e && It && ha.alternate === null && t(L, It), Jn = s(ha, Jn, Yt), an === null ? mt = ha : an.sibling = ha, an = ha, It = In;
        }
        if (Yt === j.length) {
          if (a(L, It), Pr()) {
            var Qr = Yt;
            Ys(L, Qr);
          }
          return mt;
        }
        if (It === null) {
          for (; Yt < j.length; Yt++) {
            var hi = N(L, j[Yt], le);
            hi !== null && (Jn = s(hi, Jn, Yt), an === null ? mt = hi : an.sibling = hi, an = hi);
          }
          if (Pr()) {
            var Oa = Yt;
            Ys(L, Oa);
          }
          return mt;
        }
        for (var Ma = i(L, It); Yt < j.length; Yt++) {
          var ma = A(Ma, L, Yt, j[Yt], le);
          ma !== null && (e && ma.alternate !== null && Ma.delete(ma.key === null ? Yt : ma.key), Jn = s(ma, Jn, Yt), an === null ? mt = ma : an.sibling = ma, an = ma);
        }
        if (e && Ma.forEach(function(ed) {
          return t(L, ed);
        }), Pr()) {
          var Uo = Yt;
          Ys(L, Uo);
        }
        return mt;
      }
      function ge(L, G, j, le) {
        var we = jr(j);
        if (typeof we != "function")
          throw new Error("An object is not an iterable. This error is likely caused by a bug in React. Please file an issue.");
        {
          typeof Symbol == "function" && // $FlowFixMe Flow doesn't know about toStringTag
          j[Symbol.toStringTag] === "Generator" && (Tg || y("Using Generators as children is unsupported and will likely yield unexpected results because enumerating a generator mutates it. You may convert it to an array with `Array.from()` or the `[...spread]` operator before rendering. Keep in mind you might need to polyfill these features for older browsers."), Tg = !0), j.entries === we && (Rg || y("Using Maps as children is not supported. Use an array of keyed ReactElements instead."), Rg = !0);
          var xe = we.call(j);
          if (xe)
            for (var lt = null, mt = xe.next(); !mt.done; mt = xe.next()) {
              var an = mt.value;
              lt = P(an, lt, L);
            }
        }
        var It = we.call(j);
        if (It == null)
          throw new Error("An iterable object provided no iterator.");
        for (var Jn = null, Yt = null, In = G, ha = 0, Qr = 0, hi = null, Oa = It.next(); In !== null && !Oa.done; Qr++, Oa = It.next()) {
          In.index > Qr ? (hi = In, In = null) : hi = In.sibling;
          var Ma = _(L, In, Oa.value, le);
          if (Ma === null) {
            In === null && (In = hi);
            break;
          }
          e && In && Ma.alternate === null && t(L, In), ha = s(Ma, ha, Qr), Yt === null ? Jn = Ma : Yt.sibling = Ma, Yt = Ma, In = hi;
        }
        if (Oa.done) {
          if (a(L, In), Pr()) {
            var ma = Qr;
            Ys(L, ma);
          }
          return Jn;
        }
        if (In === null) {
          for (; !Oa.done; Qr++, Oa = It.next()) {
            var Uo = N(L, Oa.value, le);
            Uo !== null && (ha = s(Uo, ha, Qr), Yt === null ? Jn = Uo : Yt.sibling = Uo, Yt = Uo);
          }
          if (Pr()) {
            var ed = Qr;
            Ys(L, ed);
          }
          return Jn;
        }
        for (var ov = i(L, In); !Oa.done; Qr++, Oa = It.next()) {
          var Xl = A(ov, L, Qr, Oa.value, le);
          Xl !== null && (e && Xl.alternate !== null && ov.delete(Xl.key === null ? Qr : Xl.key), ha = s(Xl, ha, Qr), Yt === null ? Jn = Xl : Yt.sibling = Xl, Yt = Xl);
        }
        if (e && ov.forEach(function(I_) {
          return t(L, I_);
        }), Pr()) {
          var $_ = Qr;
          Ys(L, $_);
        }
        return Jn;
      }
      function Xe(L, G, j, le) {
        if (G !== null && G.tag === $) {
          a(L, G.sibling);
          var we = o(G, j);
          return we.return = L, we;
        }
        a(L, G);
        var xe = wS(j, L.mode, le);
        return xe.return = L, xe;
      }
      function Be(L, G, j, le) {
        for (var we = j.key, xe = G; xe !== null; ) {
          if (xe.key === we) {
            var lt = j.type;
            if (lt === ba) {
              if (xe.tag === de) {
                a(L, xe.sibling);
                var mt = o(xe, j.props.children);
                return mt.return = L, mt._debugSource = j._source, mt._debugOwner = j._owner, mt;
              }
            } else if (xe.elementType === lt || // Keep this check inline so it only runs on the false path:
            IC(xe, j) || // Lazy types should reconcile their resolved type.
            // We need to do this after the Hot Reloading check above,
            // because hot reloading has different semantics than prod because
            // it doesn't resuspend. So we can't let the call below suspend.
            typeof lt == "object" && lt !== null && lt.$$typeof === Ze && Fx(lt) === xe.type) {
              a(L, xe.sibling);
              var an = o(xe, j.props);
              return an.ref = Dp(L, xe, j), an.return = L, an._debugSource = j._source, an._debugOwner = j._owner, an;
            }
            a(L, xe);
            break;
          } else
            t(L, xe);
          xe = xe.sibling;
        }
        if (j.type === ba) {
          var It = Ku(j.props.children, L.mode, le, j.key);
          return It.return = L, It;
        } else {
          var Jn = ES(j, L.mode, le);
          return Jn.ref = Dp(L, G, j), Jn.return = L, Jn;
        }
      }
      function Ht(L, G, j, le) {
        for (var we = j.key, xe = G; xe !== null; ) {
          if (xe.key === we)
            if (xe.tag === oe && xe.stateNode.containerInfo === j.containerInfo && xe.stateNode.implementation === j.implementation) {
              a(L, xe.sibling);
              var lt = o(xe, j.children || []);
              return lt.return = L, lt;
            } else {
              a(L, xe);
              break;
            }
          else
            t(L, xe);
          xe = xe.sibling;
        }
        var mt = RS(j, L.mode, le);
        return mt.return = L, mt;
      }
      function Mt(L, G, j, le) {
        var we = typeof j == "object" && j !== null && j.type === ba && j.key === null;
        if (we && (j = j.props.children), typeof j == "object" && j !== null) {
          switch (j.$$typeof) {
            case ii:
              return f(Be(L, G, j, le));
            case Lr:
              return f(Ht(L, G, j, le));
            case Ze:
              var xe = j._payload, lt = j._init;
              return Mt(L, G, lt(xe), le);
          }
          if (At(j))
            return Q(L, G, j, le);
          if (jr(j))
            return ge(L, G, j, le);
          rm(L, j);
        }
        return typeof j == "string" && j !== "" || typeof j == "number" ? f(Xe(L, G, "" + j, le)) : (typeof j == "function" && am(L), a(L, G));
      }
      return Mt;
    }
    var Af = Hx(!0), Px = Hx(!1);
    function SR(e, t) {
      if (e !== null && t.child !== e.child)
        throw new Error("Resuming work not yet implemented.");
      if (t.child !== null) {
        var a = t.child, i = ac(a, a.pendingProps);
        for (t.child = i, i.return = t; a.sibling !== null; )
          a = a.sibling, i = i.sibling = ac(a, a.pendingProps), i.return = t;
        i.sibling = null;
      }
    }
    function xR(e, t) {
      for (var a = e.child; a !== null; )
        o_(a, t), a = a.sibling;
    }
    var Ng = Uu(null), Og;
    Og = {};
    var im = null, Uf = null, Mg = null, lm = !1;
    function om() {
      im = null, Uf = null, Mg = null, lm = !1;
    }
    function Vx() {
      lm = !0;
    }
    function Bx() {
      lm = !1;
    }
    function $x(e, t, a) {
      pa(Ng, t._currentValue, e), t._currentValue = a, t._currentRenderer !== void 0 && t._currentRenderer !== null && t._currentRenderer !== Og && y("Detected multiple renderers concurrently rendering the same context provider. This is currently unsupported."), t._currentRenderer = Og;
    }
    function Lg(e, t) {
      var a = Ng.current;
      da(Ng, t), e._currentValue = a;
    }
    function jg(e, t, a) {
      for (var i = e; i !== null; ) {
        var o = i.alternate;
        if (go(i.childLanes, t) ? o !== null && !go(o.childLanes, t) && (o.childLanes = gt(o.childLanes, t)) : (i.childLanes = gt(i.childLanes, t), o !== null && (o.childLanes = gt(o.childLanes, t))), i === a)
          break;
        i = i.return;
      }
      i !== a && y("Expected to find the propagation root when scheduling context work. This error is likely caused by a bug in React. Please file an issue.");
    }
    function bR(e, t, a) {
      CR(e, t, a);
    }
    function CR(e, t, a) {
      var i = e.child;
      for (i !== null && (i.return = e); i !== null; ) {
        var o = void 0, s = i.dependencies;
        if (s !== null) {
          o = i.child;
          for (var f = s.firstContext; f !== null; ) {
            if (f.context === t) {
              if (i.tag === K) {
                var p = gu(a), v = Oo(fn, p);
                v.tag = sm;
                var g = i.updateQueue;
                if (g !== null) {
                  var x = g.shared, N = x.pending;
                  N === null ? v.next = v : (v.next = N.next, N.next = v), x.pending = v;
                }
              }
              i.lanes = gt(i.lanes, a);
              var _ = i.alternate;
              _ !== null && (_.lanes = gt(_.lanes, a)), jg(i.return, a, e), s.lanes = gt(s.lanes, a);
              break;
            }
            f = f.next;
          }
        } else if (i.tag === rt)
          o = i.type === e.type ? null : i.child;
        else if (i.tag === $e) {
          var A = i.return;
          if (A === null)
            throw new Error("We just came from a parent so we must have had a parent. This is a bug in React.");
          A.lanes = gt(A.lanes, a);
          var P = A.alternate;
          P !== null && (P.lanes = gt(P.lanes, a)), jg(A, a, e), o = i.sibling;
        } else
          o = i.child;
        if (o !== null)
          o.return = i;
        else
          for (o = i; o !== null; ) {
            if (o === e) {
              o = null;
              break;
            }
            var Q = o.sibling;
            if (Q !== null) {
              Q.return = o.return, o = Q;
              break;
            }
            o = o.return;
          }
        i = o;
      }
    }
    function Ff(e, t) {
      im = e, Uf = null, Mg = null;
      var a = e.dependencies;
      if (a !== null) {
        var i = a.firstContext;
        i !== null && (ca(a.lanes, t) && Ip(), a.firstContext = null);
      }
    }
    function ur(e) {
      lm && y("Context can only be read while React is rendering. In classes, you can read it in the render method or getDerivedStateFromProps. In function components, you can read it directly in the function body, but not inside Hooks like useReducer() or useMemo().");
      var t = e._currentValue;
      if (Mg !== e) {
        var a = {
          context: e,
          memoizedValue: t,
          next: null
        };
        if (Uf === null) {
          if (im === null)
            throw new Error("Context can only be read while React is rendering. In classes, you can read it in the render method or getDerivedStateFromProps. In function components, you can read it directly in the function body, but not inside Hooks like useReducer() or useMemo().");
          Uf = a, im.dependencies = {
            lanes: Z,
            firstContext: a
          };
        } else
          Uf = Uf.next = a;
      }
      return t;
    }
    var Xs = null;
    function zg(e) {
      Xs === null ? Xs = [e] : Xs.push(e);
    }
    function ER() {
      if (Xs !== null) {
        for (var e = 0; e < Xs.length; e++) {
          var t = Xs[e], a = t.interleaved;
          if (a !== null) {
            t.interleaved = null;
            var i = a.next, o = t.pending;
            if (o !== null) {
              var s = o.next;
              o.next = i, a.next = s;
            }
            t.pending = a;
          }
        }
        Xs = null;
      }
    }
    function Ix(e, t, a, i) {
      var o = t.interleaved;
      return o === null ? (a.next = a, zg(t)) : (a.next = o.next, o.next = a), t.interleaved = a, um(e, i);
    }
    function wR(e, t, a, i) {
      var o = t.interleaved;
      o === null ? (a.next = a, zg(t)) : (a.next = o.next, o.next = a), t.interleaved = a;
    }
    function RR(e, t, a, i) {
      var o = t.interleaved;
      return o === null ? (a.next = a, zg(t)) : (a.next = o.next, o.next = a), t.interleaved = a, um(e, i);
    }
    function Ja(e, t) {
      return um(e, t);
    }
    var TR = um;
    function um(e, t) {
      e.lanes = gt(e.lanes, t);
      var a = e.alternate;
      a !== null && (a.lanes = gt(a.lanes, t)), a === null && (e.flags & (pn | Pa)) !== qe && PC(e);
      for (var i = e, o = e.return; o !== null; )
        o.childLanes = gt(o.childLanes, t), a = o.alternate, a !== null ? a.childLanes = gt(a.childLanes, t) : (o.flags & (pn | Pa)) !== qe && PC(e), i = o, o = o.return;
      if (i.tag === ne) {
        var s = i.stateNode;
        return s;
      } else
        return null;
    }
    var Yx = 0, Wx = 1, sm = 2, Ag = 3, cm = !1, Ug, fm;
    Ug = !1, fm = null;
    function Fg(e) {
      var t = {
        baseState: e.memoizedState,
        firstBaseUpdate: null,
        lastBaseUpdate: null,
        shared: {
          pending: null,
          interleaved: null,
          lanes: Z
        },
        effects: null
      };
      e.updateQueue = t;
    }
    function Qx(e, t) {
      var a = t.updateQueue, i = e.updateQueue;
      if (a === i) {
        var o = {
          baseState: i.baseState,
          firstBaseUpdate: i.firstBaseUpdate,
          lastBaseUpdate: i.lastBaseUpdate,
          shared: i.shared,
          effects: i.effects
        };
        t.updateQueue = o;
      }
    }
    function Oo(e, t) {
      var a = {
        eventTime: e,
        lane: t,
        tag: Yx,
        payload: null,
        callback: null,
        next: null
      };
      return a;
    }
    function Vu(e, t, a) {
      var i = e.updateQueue;
      if (i === null)
        return null;
      var o = i.shared;
      if (fm === o && !Ug && (y("An update (setState, replaceState, or forceUpdate) was scheduled from inside an update function. Update functions should be pure, with zero side-effects. Consider using componentDidUpdate or a callback."), Ug = !0), wk()) {
        var s = o.pending;
        return s === null ? t.next = t : (t.next = s.next, s.next = t), o.pending = t, TR(e, a);
      } else
        return RR(e, o, t, a);
    }
    function dm(e, t, a) {
      var i = t.updateQueue;
      if (i !== null) {
        var o = i.shared;
        if (Id(a)) {
          var s = o.lanes;
          s = ef(s, e.pendingLanes);
          var f = gt(s, a);
          o.lanes = f, Yd(e, f);
        }
      }
    }
    function Hg(e, t) {
      var a = e.updateQueue, i = e.alternate;
      if (i !== null) {
        var o = i.updateQueue;
        if (a === o) {
          var s = null, f = null, p = a.firstBaseUpdate;
          if (p !== null) {
            var v = p;
            do {
              var g = {
                eventTime: v.eventTime,
                lane: v.lane,
                tag: v.tag,
                payload: v.payload,
                callback: v.callback,
                next: null
              };
              f === null ? s = f = g : (f.next = g, f = g), v = v.next;
            } while (v !== null);
            f === null ? s = f = t : (f.next = t, f = t);
          } else
            s = f = t;
          a = {
            baseState: o.baseState,
            firstBaseUpdate: s,
            lastBaseUpdate: f,
            shared: o.shared,
            effects: o.effects
          }, e.updateQueue = a;
          return;
        }
      }
      var x = a.lastBaseUpdate;
      x === null ? a.firstBaseUpdate = t : x.next = t, a.lastBaseUpdate = t;
    }
    function kR(e, t, a, i, o, s) {
      switch (a.tag) {
        case Wx: {
          var f = a.payload;
          if (typeof f == "function") {
            Vx();
            var p = f.call(s, i, o);
            {
              if (e.mode & _t) {
                Bn(!0);
                try {
                  f.call(s, i, o);
                } finally {
                  Bn(!1);
                }
              }
              Bx();
            }
            return p;
          }
          return f;
        }
        case Ag:
          e.flags = e.flags & ~ar | ot;
        case Yx: {
          var v = a.payload, g;
          if (typeof v == "function") {
            Vx(), g = v.call(s, i, o);
            {
              if (e.mode & _t) {
                Bn(!0);
                try {
                  v.call(s, i, o);
                } finally {
                  Bn(!1);
                }
              }
              Bx();
            }
          } else
            g = v;
          return g == null ? i : Et({}, i, g);
        }
        case sm:
          return cm = !0, i;
      }
      return i;
    }
    function pm(e, t, a, i) {
      var o = e.updateQueue;
      cm = !1, fm = o.shared;
      var s = o.firstBaseUpdate, f = o.lastBaseUpdate, p = o.shared.pending;
      if (p !== null) {
        o.shared.pending = null;
        var v = p, g = v.next;
        v.next = null, f === null ? s = g : f.next = g, f = v;
        var x = e.alternate;
        if (x !== null) {
          var N = x.updateQueue, _ = N.lastBaseUpdate;
          _ !== f && (_ === null ? N.firstBaseUpdate = g : _.next = g, N.lastBaseUpdate = v);
        }
      }
      if (s !== null) {
        var A = o.baseState, P = Z, Q = null, ge = null, Xe = null, Be = s;
        do {
          var Ht = Be.lane, Mt = Be.eventTime;
          if (go(i, Ht)) {
            if (Xe !== null) {
              var G = {
                eventTime: Mt,
                // This update is going to be committed so we never want uncommit
                // it. Using NoLane works because 0 is a subset of all bitmasks, so
                // this will never be skipped by the check above.
                lane: $n,
                tag: Be.tag,
                payload: Be.payload,
                callback: Be.callback,
                next: null
              };
              Xe = Xe.next = G;
            }
            A = kR(e, o, Be, A, t, a);
            var j = Be.callback;
            if (j !== null && // If the update was already committed, we should not queue its
            // callback again.
            Be.lane !== $n) {
              e.flags |= wi;
              var le = o.effects;
              le === null ? o.effects = [Be] : le.push(Be);
            }
          } else {
            var L = {
              eventTime: Mt,
              lane: Ht,
              tag: Be.tag,
              payload: Be.payload,
              callback: Be.callback,
              next: null
            };
            Xe === null ? (ge = Xe = L, Q = A) : Xe = Xe.next = L, P = gt(P, Ht);
          }
          if (Be = Be.next, Be === null) {
            if (p = o.shared.pending, p === null)
              break;
            var we = p, xe = we.next;
            we.next = null, Be = xe, o.lastBaseUpdate = we, o.shared.pending = null;
          }
        } while (!0);
        Xe === null && (Q = A), o.baseState = Q, o.firstBaseUpdate = ge, o.lastBaseUpdate = Xe;
        var lt = o.shared.interleaved;
        if (lt !== null) {
          var mt = lt;
          do
            P = gt(P, mt.lane), mt = mt.next;
          while (mt !== lt);
        } else
          s === null && (o.shared.lanes = Z);
        nv(P), e.lanes = P, e.memoizedState = A;
      }
      fm = null;
    }
    function _R(e, t) {
      if (typeof e != "function")
        throw new Error("Invalid argument passed as callback. Expected a function. Instead " + ("received: " + e));
      e.call(t);
    }
    function Gx() {
      cm = !1;
    }
    function vm() {
      return cm;
    }
    function qx(e, t, a) {
      var i = t.effects;
      if (t.effects = null, i !== null)
        for (var o = 0; o < i.length; o++) {
          var s = i[o], f = s.callback;
          f !== null && (s.callback = null, _R(f, a));
        }
    }
    var Np = {}, Bu = Uu(Np), Op = Uu(Np), hm = Uu(Np);
    function mm(e) {
      if (e === Np)
        throw new Error("Expected host context to exist. This error is likely caused by a bug in React. Please file an issue.");
      return e;
    }
    function Xx() {
      var e = mm(hm.current);
      return e;
    }
    function Pg(e, t) {
      pa(hm, t, e), pa(Op, e, e), pa(Bu, Np, e);
      var a = Y1(t);
      da(Bu, e), pa(Bu, a, e);
    }
    function Hf(e) {
      da(Bu, e), da(Op, e), da(hm, e);
    }
    function Vg() {
      var e = mm(Bu.current);
      return e;
    }
    function Kx(e) {
      mm(hm.current);
      var t = mm(Bu.current), a = W1(t, e.type);
      t !== a && (pa(Op, e, e), pa(Bu, a, e));
    }
    function Bg(e) {
      Op.current === e && (da(Bu, e), da(Op, e));
    }
    var DR = 0, Jx = 1, Zx = 1, Mp = 2, il = Uu(DR);
    function $g(e, t) {
      return (e & t) !== 0;
    }
    function Pf(e) {
      return e & Jx;
    }
    function Ig(e, t) {
      return e & Jx | t;
    }
    function NR(e, t) {
      return e | t;
    }
    function $u(e, t) {
      pa(il, t, e);
    }
    function Vf(e) {
      da(il, e);
    }
    function OR(e, t) {
      var a = e.memoizedState;
      return a !== null ? a.dehydrated !== null : (e.memoizedProps, !0);
    }
    function ym(e) {
      for (var t = e; t !== null; ) {
        if (t.tag === ke) {
          var a = t.memoizedState;
          if (a !== null) {
            var i = a.dehydrated;
            if (i === null || mx(i) || ug(i))
              return t;
          }
        } else if (t.tag === it && // revealOrder undefined can't be trusted because it don't
        // keep track of whether it suspended or not.
        t.memoizedProps.revealOrder !== void 0) {
          var o = (t.flags & ot) !== qe;
          if (o)
            return t;
        } else if (t.child !== null) {
          t.child.return = t, t = t.child;
          continue;
        }
        if (t === e)
          return null;
        for (; t.sibling === null; ) {
          if (t.return === null || t.return === e)
            return null;
          t = t.return;
        }
        t.sibling.return = t.return, t = t.sibling;
      }
      return null;
    }
    var Za = (
      /*   */
      0
    ), pr = (
      /* */
      1
    ), $l = (
      /*  */
      2
    ), vr = (
      /*    */
      4
    ), Vr = (
      /*   */
      8
    ), Yg = [];
    function Wg() {
      for (var e = 0; e < Yg.length; e++) {
        var t = Yg[e];
        t._workInProgressVersionPrimary = null;
      }
      Yg.length = 0;
    }
    function MR(e, t) {
      var a = t._getVersion, i = a(t._source);
      e.mutableSourceEagerHydrationData == null ? e.mutableSourceEagerHydrationData = [t, i] : e.mutableSourceEagerHydrationData.push(t, i);
    }
    var Ee = b.ReactCurrentDispatcher, Lp = b.ReactCurrentBatchConfig, Qg, Bf;
    Qg = /* @__PURE__ */ new Set();
    var Ks = Z, rn = null, hr = null, mr = null, gm = !1, jp = !1, zp = 0, LR = 0, jR = 25, J = null, Li = null, Iu = -1, Gg = !1;
    function en() {
      {
        var e = J;
        Li === null ? Li = [e] : Li.push(e);
      }
    }
    function he() {
      {
        var e = J;
        Li !== null && (Iu++, Li[Iu] !== e && zR(e));
      }
    }
    function $f(e) {
      e != null && !At(e) && y("%s received a final argument that is not an array (instead, received `%s`). When specified, the final argument must be an array.", J, typeof e);
    }
    function zR(e) {
      {
        var t = dt(rn);
        if (!Qg.has(t) && (Qg.add(t), Li !== null)) {
          for (var a = "", i = 30, o = 0; o <= Iu; o++) {
            for (var s = Li[o], f = o === Iu ? e : s, p = o + 1 + ". " + s; p.length < i; )
              p += " ";
            p += f + `
`, a += p;
          }
          y(`React has detected a change in the order of Hooks called by %s. This will lead to bugs and errors if not fixed. For more information, read the Rules of Hooks: https://reactjs.org/link/rules-of-hooks

   Previous render            Next render
   ------------------------------------------------------
%s   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
`, t, a);
        }
      }
    }
    function va() {
      throw new Error(`Invalid hook call. Hooks can only be called inside of the body of a function component. This could happen for one of the following reasons:
1. You might have mismatching versions of React and the renderer (such as React DOM)
2. You might be breaking the Rules of Hooks
3. You might have more than one copy of React in the same app
See https://reactjs.org/link/invalid-hook-call for tips about how to debug and fix this problem.`);
    }
    function qg(e, t) {
      if (Gg)
        return !1;
      if (t === null)
        return y("%s received a final argument during this render, but not during the previous render. Even though the final argument is optional, its type cannot change between renders.", J), !1;
      e.length !== t.length && y(`The final argument passed to %s changed size between renders. The order and size of this array must remain constant.

Previous: %s
Incoming: %s`, J, "[" + t.join(", ") + "]", "[" + e.join(", ") + "]");
      for (var a = 0; a < t.length && a < e.length; a++)
        if (!De(e[a], t[a]))
          return !1;
      return !0;
    }
    function If(e, t, a, i, o, s) {
      Ks = s, rn = t, Li = e !== null ? e._debugHookTypes : null, Iu = -1, Gg = e !== null && e.type !== t.type, t.memoizedState = null, t.updateQueue = null, t.lanes = Z, e !== null && e.memoizedState !== null ? Ee.current = bb : Li !== null ? Ee.current = xb : Ee.current = Sb;
      var f = a(i, o);
      if (jp) {
        var p = 0;
        do {
          if (jp = !1, zp = 0, p >= jR)
            throw new Error("Too many re-renders. React limits the number of renders to prevent an infinite loop.");
          p += 1, Gg = !1, hr = null, mr = null, t.updateQueue = null, Iu = -1, Ee.current = Cb, f = a(i, o);
        } while (jp);
      }
      Ee.current = Om, t._debugHookTypes = Li;
      var v = hr !== null && hr.next !== null;
      if (Ks = Z, rn = null, hr = null, mr = null, J = null, Li = null, Iu = -1, e !== null && (e.flags & cr) !== (t.flags & cr) && // Disable this warning in legacy mode, because legacy Suspense is weird
      // and creates false positives. To make this work in legacy mode, we'd
      // need to mark fibers that commit in an incomplete state, somehow. For
      // now I'll disable the warning that most of the bugs that would trigger
      // it are either exclusive to concurrent mode or exist in both.
      (e.mode & Ve) !== Fe && y("Internal React error: Expected static flag was missing. Please notify the React team."), gm = !1, v)
        throw new Error("Rendered fewer hooks than expected. This may be caused by an accidental early return statement.");
      return f;
    }
    function Yf() {
      var e = zp !== 0;
      return zp = 0, e;
    }
    function eb(e, t, a) {
      t.updateQueue = e.updateQueue, (t.mode & Ta) !== Fe ? t.flags &= ~(uo | aa | yn | xt) : t.flags &= ~(yn | xt), e.lanes = _s(e.lanes, a);
    }
    function tb() {
      if (Ee.current = Om, gm) {
        for (var e = rn.memoizedState; e !== null; ) {
          var t = e.queue;
          t !== null && (t.pending = null), e = e.next;
        }
        gm = !1;
      }
      Ks = Z, rn = null, hr = null, mr = null, Li = null, Iu = -1, J = null, vb = !1, jp = !1, zp = 0;
    }
    function Il() {
      var e = {
        memoizedState: null,
        baseState: null,
        baseQueue: null,
        queue: null,
        next: null
      };
      return mr === null ? rn.memoizedState = mr = e : mr = mr.next = e, mr;
    }
    function ji() {
      var e;
      if (hr === null) {
        var t = rn.alternate;
        t !== null ? e = t.memoizedState : e = null;
      } else
        e = hr.next;
      var a;
      if (mr === null ? a = rn.memoizedState : a = mr.next, a !== null)
        mr = a, a = mr.next, hr = e;
      else {
        if (e === null)
          throw new Error("Rendered more hooks than during the previous render.");
        hr = e;
        var i = {
          memoizedState: hr.memoizedState,
          baseState: hr.baseState,
          baseQueue: hr.baseQueue,
          queue: hr.queue,
          next: null
        };
        mr === null ? rn.memoizedState = mr = i : mr = mr.next = i;
      }
      return mr;
    }
    function nb() {
      return {
        lastEffect: null,
        stores: null
      };
    }
    function Xg(e, t) {
      return typeof t == "function" ? t(e) : t;
    }
    function Kg(e, t, a) {
      var i = Il(), o;
      a !== void 0 ? o = a(t) : o = t, i.memoizedState = i.baseState = o;
      var s = {
        pending: null,
        interleaved: null,
        lanes: Z,
        dispatch: null,
        lastRenderedReducer: e,
        lastRenderedState: o
      };
      i.queue = s;
      var f = s.dispatch = HR.bind(null, rn, s);
      return [i.memoizedState, f];
    }
    function Jg(e, t, a) {
      var i = ji(), o = i.queue;
      if (o === null)
        throw new Error("Should have a queue. This is likely a bug in React. Please file an issue.");
      o.lastRenderedReducer = e;
      var s = hr, f = s.baseQueue, p = o.pending;
      if (p !== null) {
        if (f !== null) {
          var v = f.next, g = p.next;
          f.next = g, p.next = v;
        }
        s.baseQueue !== f && y("Internal error: Expected work-in-progress queue to be a clone. This is a bug in React."), s.baseQueue = f = p, o.pending = null;
      }
      if (f !== null) {
        var x = f.next, N = s.baseState, _ = null, A = null, P = null, Q = x;
        do {
          var ge = Q.lane;
          if (go(Ks, ge)) {
            if (P !== null) {
              var Be = {
                // This update is going to be committed so we never want uncommit
                // it. Using NoLane works because 0 is a subset of all bitmasks, so
                // this will never be skipped by the check above.
                lane: $n,
                action: Q.action,
                hasEagerState: Q.hasEagerState,
                eagerState: Q.eagerState,
                next: null
              };
              P = P.next = Be;
            }
            if (Q.hasEagerState)
              N = Q.eagerState;
            else {
              var Ht = Q.action;
              N = e(N, Ht);
            }
          } else {
            var Xe = {
              lane: ge,
              action: Q.action,
              hasEagerState: Q.hasEagerState,
              eagerState: Q.eagerState,
              next: null
            };
            P === null ? (A = P = Xe, _ = N) : P = P.next = Xe, rn.lanes = gt(rn.lanes, ge), nv(ge);
          }
          Q = Q.next;
        } while (Q !== null && Q !== x);
        P === null ? _ = N : P.next = A, De(N, i.memoizedState) || Ip(), i.memoizedState = N, i.baseState = _, i.baseQueue = P, o.lastRenderedState = N;
      }
      var Mt = o.interleaved;
      if (Mt !== null) {
        var L = Mt;
        do {
          var G = L.lane;
          rn.lanes = gt(rn.lanes, G), nv(G), L = L.next;
        } while (L !== Mt);
      } else
        f === null && (o.lanes = Z);
      var j = o.dispatch;
      return [i.memoizedState, j];
    }
    function Zg(e, t, a) {
      var i = ji(), o = i.queue;
      if (o === null)
        throw new Error("Should have a queue. This is likely a bug in React. Please file an issue.");
      o.lastRenderedReducer = e;
      var s = o.dispatch, f = o.pending, p = i.memoizedState;
      if (f !== null) {
        o.pending = null;
        var v = f.next, g = v;
        do {
          var x = g.action;
          p = e(p, x), g = g.next;
        } while (g !== v);
        De(p, i.memoizedState) || Ip(), i.memoizedState = p, i.baseQueue === null && (i.baseState = p), o.lastRenderedState = p;
      }
      return [p, s];
    }
    function CN(e, t, a) {
    }
    function EN(e, t, a) {
    }
    function e0(e, t, a) {
      var i = rn, o = Il(), s, f = Pr();
      if (f) {
        if (a === void 0)
          throw new Error("Missing getServerSnapshot, which is required for server-rendered content. Will revert to client rendering.");
        s = a(), Bf || s !== a() && (y("The result of getServerSnapshot should be cached to avoid an infinite loop"), Bf = !0);
      } else {
        if (s = t(), !Bf) {
          var p = t();
          De(s, p) || (y("The result of getSnapshot should be cached to avoid an infinite loop"), Bf = !0);
        }
        var v = Xm();
        if (v === null)
          throw new Error("Expected a work-in-progress root. This is a bug in React. Please file an issue.");
        ks(v, Ks) || rb(i, t, s);
      }
      o.memoizedState = s;
      var g = {
        value: s,
        getSnapshot: t
      };
      return o.queue = g, Em(ib.bind(null, i, g, e), [e]), i.flags |= yn, Ap(pr | Vr, ab.bind(null, i, g, s, t), void 0, null), s;
    }
    function Sm(e, t, a) {
      var i = rn, o = ji(), s = t();
      if (!Bf) {
        var f = t();
        De(s, f) || (y("The result of getSnapshot should be cached to avoid an infinite loop"), Bf = !0);
      }
      var p = o.memoizedState, v = !De(p, s);
      v && (o.memoizedState = s, Ip());
      var g = o.queue;
      if (Fp(ib.bind(null, i, g, e), [e]), g.getSnapshot !== t || v || // Check if the susbcribe function changed. We can save some memory by
      // checking whether we scheduled a subscription effect above.
      mr !== null && mr.memoizedState.tag & pr) {
        i.flags |= yn, Ap(pr | Vr, ab.bind(null, i, g, s, t), void 0, null);
        var x = Xm();
        if (x === null)
          throw new Error("Expected a work-in-progress root. This is a bug in React. Please file an issue.");
        ks(x, Ks) || rb(i, t, s);
      }
      return s;
    }
    function rb(e, t, a) {
      e.flags |= ys;
      var i = {
        getSnapshot: t,
        value: a
      }, o = rn.updateQueue;
      if (o === null)
        o = nb(), rn.updateQueue = o, o.stores = [i];
      else {
        var s = o.stores;
        s === null ? o.stores = [i] : s.push(i);
      }
    }
    function ab(e, t, a, i) {
      t.value = a, t.getSnapshot = i, lb(t) && ob(e);
    }
    function ib(e, t, a) {
      var i = function() {
        lb(t) && ob(e);
      };
      return a(i);
    }
    function lb(e) {
      var t = e.getSnapshot, a = e.value;
      try {
        var i = t();
        return !De(a, i);
      } catch {
        return !0;
      }
    }
    function ob(e) {
      var t = Ja(e, Qe);
      t !== null && xr(t, e, Qe, fn);
    }
    function xm(e) {
      var t = Il();
      typeof e == "function" && (e = e()), t.memoizedState = t.baseState = e;
      var a = {
        pending: null,
        interleaved: null,
        lanes: Z,
        dispatch: null,
        lastRenderedReducer: Xg,
        lastRenderedState: e
      };
      t.queue = a;
      var i = a.dispatch = PR.bind(null, rn, a);
      return [t.memoizedState, i];
    }
    function t0(e) {
      return Jg(Xg);
    }
    function n0(e) {
      return Zg(Xg);
    }
    function Ap(e, t, a, i) {
      var o = {
        tag: e,
        create: t,
        destroy: a,
        deps: i,
        // Circular
        next: null
      }, s = rn.updateQueue;
      if (s === null)
        s = nb(), rn.updateQueue = s, s.lastEffect = o.next = o;
      else {
        var f = s.lastEffect;
        if (f === null)
          s.lastEffect = o.next = o;
        else {
          var p = f.next;
          f.next = o, o.next = p, s.lastEffect = o;
        }
      }
      return o;
    }
    function r0(e) {
      var t = Il();
      {
        var a = {
          current: e
        };
        return t.memoizedState = a, a;
      }
    }
    function bm(e) {
      var t = ji();
      return t.memoizedState;
    }
    function Up(e, t, a, i) {
      var o = Il(), s = i === void 0 ? null : i;
      rn.flags |= e, o.memoizedState = Ap(pr | t, a, void 0, s);
    }
    function Cm(e, t, a, i) {
      var o = ji(), s = i === void 0 ? null : i, f = void 0;
      if (hr !== null) {
        var p = hr.memoizedState;
        if (f = p.destroy, s !== null) {
          var v = p.deps;
          if (qg(s, v)) {
            o.memoizedState = Ap(t, a, f, s);
            return;
          }
        }
      }
      rn.flags |= e, o.memoizedState = Ap(pr | t, a, f, s);
    }
    function Em(e, t) {
      return (rn.mode & Ta) !== Fe ? Up(uo | yn | Ol, Vr, e, t) : Up(yn | Ol, Vr, e, t);
    }
    function Fp(e, t) {
      return Cm(yn, Vr, e, t);
    }
    function a0(e, t) {
      return Up(xt, $l, e, t);
    }
    function wm(e, t) {
      return Cm(xt, $l, e, t);
    }
    function i0(e, t) {
      var a = xt;
      return a |= ra, (rn.mode & Ta) !== Fe && (a |= aa), Up(a, vr, e, t);
    }
    function Rm(e, t) {
      return Cm(xt, vr, e, t);
    }
    function ub(e, t) {
      if (typeof t == "function") {
        var a = t, i = e();
        return a(i), function() {
          a(null);
        };
      } else if (t != null) {
        var o = t;
        o.hasOwnProperty("current") || y("Expected useImperativeHandle() first argument to either be a ref callback or React.createRef() object. Instead received: %s.", "an object with keys {" + Object.keys(o).join(", ") + "}");
        var s = e();
        return o.current = s, function() {
          o.current = null;
        };
      }
    }
    function l0(e, t, a) {
      typeof t != "function" && y("Expected useImperativeHandle() second argument to be a function that creates a handle. Instead received: %s.", t !== null ? typeof t : "null");
      var i = a != null ? a.concat([e]) : null, o = xt;
      return o |= ra, (rn.mode & Ta) !== Fe && (o |= aa), Up(o, vr, ub.bind(null, t, e), i);
    }
    function Tm(e, t, a) {
      typeof t != "function" && y("Expected useImperativeHandle() second argument to be a function that creates a handle. Instead received: %s.", t !== null ? typeof t : "null");
      var i = a != null ? a.concat([e]) : null;
      return Cm(xt, vr, ub.bind(null, t, e), i);
    }
    function AR(e, t) {
    }
    var km = AR;
    function o0(e, t) {
      var a = Il(), i = t === void 0 ? null : t;
      return a.memoizedState = [e, i], e;
    }
    function _m(e, t) {
      var a = ji(), i = t === void 0 ? null : t, o = a.memoizedState;
      if (o !== null && i !== null) {
        var s = o[1];
        if (qg(i, s))
          return o[0];
      }
      return a.memoizedState = [e, i], e;
    }
    function u0(e, t) {
      var a = Il(), i = t === void 0 ? null : t, o = e();
      return a.memoizedState = [o, i], o;
    }
    function Dm(e, t) {
      var a = ji(), i = t === void 0 ? null : t, o = a.memoizedState;
      if (o !== null && i !== null) {
        var s = o[1];
        if (qg(i, s))
          return o[0];
      }
      var f = e();
      return a.memoizedState = [f, i], f;
    }
    function s0(e) {
      var t = Il();
      return t.memoizedState = e, e;
    }
    function sb(e) {
      var t = ji(), a = hr, i = a.memoizedState;
      return fb(t, i, e);
    }
    function cb(e) {
      var t = ji();
      if (hr === null)
        return t.memoizedState = e, e;
      var a = hr.memoizedState;
      return fb(t, a, e);
    }
    function fb(e, t, a) {
      var i = !ih(Ks);
      if (i) {
        if (!De(a, t)) {
          var o = uh();
          rn.lanes = gt(rn.lanes, o), nv(o), e.baseState = !0;
        }
        return t;
      } else
        return e.baseState && (e.baseState = !1, Ip()), e.memoizedState = a, a;
    }
    function UR(e, t, a) {
      var i = Wa();
      Dn(Dy(i, Ji)), e(!0);
      var o = Lp.transition;
      Lp.transition = {};
      var s = Lp.transition;
      Lp.transition._updatedFibers = /* @__PURE__ */ new Set();
      try {
        e(!1), t();
      } finally {
        if (Dn(i), Lp.transition = o, o === null && s._updatedFibers) {
          var f = s._updatedFibers.size;
          f > 10 && W("Detected a large number of updates inside startTransition. If this is due to a subscription please re-write it to use React provided hooks. Otherwise concurrent mode guarantees are off the table."), s._updatedFibers.clear();
        }
      }
    }
    function c0() {
      var e = xm(!1), t = e[0], a = e[1], i = UR.bind(null, a), o = Il();
      return o.memoizedState = i, [t, i];
    }
    function db() {
      var e = t0(), t = e[0], a = ji(), i = a.memoizedState;
      return [t, i];
    }
    function pb() {
      var e = n0(), t = e[0], a = ji(), i = a.memoizedState;
      return [t, i];
    }
    var vb = !1;
    function FR() {
      return vb;
    }
    function f0() {
      var e = Il(), t = Xm(), a = t.identifierPrefix, i;
      if (Pr()) {
        var o = tR();
        i = ":" + a + "R" + o;
        var s = zp++;
        s > 0 && (i += "H" + s.toString(32)), i += ":";
      } else {
        var f = LR++;
        i = ":" + a + "r" + f.toString(32) + ":";
      }
      return e.memoizedState = i, i;
    }
    function Nm() {
      var e = ji(), t = e.memoizedState;
      return t;
    }
    function HR(e, t, a) {
      typeof arguments[3] == "function" && y("State updates from the useState() and useReducer() Hooks don't support the second callback argument. To execute a side effect after rendering, declare it in the component body with useEffect().");
      var i = qu(e), o = {
        lane: i,
        action: a,
        hasEagerState: !1,
        eagerState: null,
        next: null
      };
      if (hb(e))
        mb(t, o);
      else {
        var s = Ix(e, t, o, i);
        if (s !== null) {
          var f = Na();
          xr(s, e, i, f), yb(s, t, i);
        }
      }
      gb(e, i);
    }
    function PR(e, t, a) {
      typeof arguments[3] == "function" && y("State updates from the useState() and useReducer() Hooks don't support the second callback argument. To execute a side effect after rendering, declare it in the component body with useEffect().");
      var i = qu(e), o = {
        lane: i,
        action: a,
        hasEagerState: !1,
        eagerState: null,
        next: null
      };
      if (hb(e))
        mb(t, o);
      else {
        var s = e.alternate;
        if (e.lanes === Z && (s === null || s.lanes === Z)) {
          var f = t.lastRenderedReducer;
          if (f !== null) {
            var p;
            p = Ee.current, Ee.current = ll;
            try {
              var v = t.lastRenderedState, g = f(v, a);
              if (o.hasEagerState = !0, o.eagerState = g, De(g, v)) {
                wR(e, t, o, i);
                return;
              }
            } catch {
            } finally {
              Ee.current = p;
            }
          }
        }
        var x = Ix(e, t, o, i);
        if (x !== null) {
          var N = Na();
          xr(x, e, i, N), yb(x, t, i);
        }
      }
      gb(e, i);
    }
    function hb(e) {
      var t = e.alternate;
      return e === rn || t !== null && t === rn;
    }
    function mb(e, t) {
      jp = gm = !0;
      var a = e.pending;
      a === null ? t.next = t : (t.next = a.next, a.next = t), e.pending = t;
    }
    function yb(e, t, a) {
      if (Id(a)) {
        var i = t.lanes;
        i = ef(i, e.pendingLanes);
        var o = gt(i, a);
        t.lanes = o, Yd(e, o);
      }
    }
    function gb(e, t, a) {
      bs(e, t);
    }
    var Om = {
      readContext: ur,
      useCallback: va,
      useContext: va,
      useEffect: va,
      useImperativeHandle: va,
      useInsertionEffect: va,
      useLayoutEffect: va,
      useMemo: va,
      useReducer: va,
      useRef: va,
      useState: va,
      useDebugValue: va,
      useDeferredValue: va,
      useTransition: va,
      useMutableSource: va,
      useSyncExternalStore: va,
      useId: va,
      unstable_isNewReconciler: I
    }, Sb = null, xb = null, bb = null, Cb = null, Yl = null, ll = null, Mm = null;
    {
      var d0 = function() {
        y("Context can only be read while React is rendering. In classes, you can read it in the render method or getDerivedStateFromProps. In function components, you can read it directly in the function body, but not inside Hooks like useReducer() or useMemo().");
      }, pt = function() {
        y("Do not call Hooks inside useEffect(...), useMemo(...), or other built-in Hooks. You can only call Hooks at the top level of your React function. For more information, see https://reactjs.org/link/rules-of-hooks");
      };
      Sb = {
        readContext: function(e) {
          return ur(e);
        },
        useCallback: function(e, t) {
          return J = "useCallback", en(), $f(t), o0(e, t);
        },
        useContext: function(e) {
          return J = "useContext", en(), ur(e);
        },
        useEffect: function(e, t) {
          return J = "useEffect", en(), $f(t), Em(e, t);
        },
        useImperativeHandle: function(e, t, a) {
          return J = "useImperativeHandle", en(), $f(a), l0(e, t, a);
        },
        useInsertionEffect: function(e, t) {
          return J = "useInsertionEffect", en(), $f(t), a0(e, t);
        },
        useLayoutEffect: function(e, t) {
          return J = "useLayoutEffect", en(), $f(t), i0(e, t);
        },
        useMemo: function(e, t) {
          J = "useMemo", en(), $f(t);
          var a = Ee.current;
          Ee.current = Yl;
          try {
            return u0(e, t);
          } finally {
            Ee.current = a;
          }
        },
        useReducer: function(e, t, a) {
          J = "useReducer", en();
          var i = Ee.current;
          Ee.current = Yl;
          try {
            return Kg(e, t, a);
          } finally {
            Ee.current = i;
          }
        },
        useRef: function(e) {
          return J = "useRef", en(), r0(e);
        },
        useState: function(e) {
          J = "useState", en();
          var t = Ee.current;
          Ee.current = Yl;
          try {
            return xm(e);
          } finally {
            Ee.current = t;
          }
        },
        useDebugValue: function(e, t) {
          return J = "useDebugValue", en(), void 0;
        },
        useDeferredValue: function(e) {
          return J = "useDeferredValue", en(), s0(e);
        },
        useTransition: function() {
          return J = "useTransition", en(), c0();
        },
        useMutableSource: function(e, t, a) {
          return J = "useMutableSource", en(), void 0;
        },
        useSyncExternalStore: function(e, t, a) {
          return J = "useSyncExternalStore", en(), e0(e, t, a);
        },
        useId: function() {
          return J = "useId", en(), f0();
        },
        unstable_isNewReconciler: I
      }, xb = {
        readContext: function(e) {
          return ur(e);
        },
        useCallback: function(e, t) {
          return J = "useCallback", he(), o0(e, t);
        },
        useContext: function(e) {
          return J = "useContext", he(), ur(e);
        },
        useEffect: function(e, t) {
          return J = "useEffect", he(), Em(e, t);
        },
        useImperativeHandle: function(e, t, a) {
          return J = "useImperativeHandle", he(), l0(e, t, a);
        },
        useInsertionEffect: function(e, t) {
          return J = "useInsertionEffect", he(), a0(e, t);
        },
        useLayoutEffect: function(e, t) {
          return J = "useLayoutEffect", he(), i0(e, t);
        },
        useMemo: function(e, t) {
          J = "useMemo", he();
          var a = Ee.current;
          Ee.current = Yl;
          try {
            return u0(e, t);
          } finally {
            Ee.current = a;
          }
        },
        useReducer: function(e, t, a) {
          J = "useReducer", he();
          var i = Ee.current;
          Ee.current = Yl;
          try {
            return Kg(e, t, a);
          } finally {
            Ee.current = i;
          }
        },
        useRef: function(e) {
          return J = "useRef", he(), r0(e);
        },
        useState: function(e) {
          J = "useState", he();
          var t = Ee.current;
          Ee.current = Yl;
          try {
            return xm(e);
          } finally {
            Ee.current = t;
          }
        },
        useDebugValue: function(e, t) {
          return J = "useDebugValue", he(), void 0;
        },
        useDeferredValue: function(e) {
          return J = "useDeferredValue", he(), s0(e);
        },
        useTransition: function() {
          return J = "useTransition", he(), c0();
        },
        useMutableSource: function(e, t, a) {
          return J = "useMutableSource", he(), void 0;
        },
        useSyncExternalStore: function(e, t, a) {
          return J = "useSyncExternalStore", he(), e0(e, t, a);
        },
        useId: function() {
          return J = "useId", he(), f0();
        },
        unstable_isNewReconciler: I
      }, bb = {
        readContext: function(e) {
          return ur(e);
        },
        useCallback: function(e, t) {
          return J = "useCallback", he(), _m(e, t);
        },
        useContext: function(e) {
          return J = "useContext", he(), ur(e);
        },
        useEffect: function(e, t) {
          return J = "useEffect", he(), Fp(e, t);
        },
        useImperativeHandle: function(e, t, a) {
          return J = "useImperativeHandle", he(), Tm(e, t, a);
        },
        useInsertionEffect: function(e, t) {
          return J = "useInsertionEffect", he(), wm(e, t);
        },
        useLayoutEffect: function(e, t) {
          return J = "useLayoutEffect", he(), Rm(e, t);
        },
        useMemo: function(e, t) {
          J = "useMemo", he();
          var a = Ee.current;
          Ee.current = ll;
          try {
            return Dm(e, t);
          } finally {
            Ee.current = a;
          }
        },
        useReducer: function(e, t, a) {
          J = "useReducer", he();
          var i = Ee.current;
          Ee.current = ll;
          try {
            return Jg(e, t, a);
          } finally {
            Ee.current = i;
          }
        },
        useRef: function(e) {
          return J = "useRef", he(), bm();
        },
        useState: function(e) {
          J = "useState", he();
          var t = Ee.current;
          Ee.current = ll;
          try {
            return t0(e);
          } finally {
            Ee.current = t;
          }
        },
        useDebugValue: function(e, t) {
          return J = "useDebugValue", he(), km();
        },
        useDeferredValue: function(e) {
          return J = "useDeferredValue", he(), sb(e);
        },
        useTransition: function() {
          return J = "useTransition", he(), db();
        },
        useMutableSource: function(e, t, a) {
          return J = "useMutableSource", he(), void 0;
        },
        useSyncExternalStore: function(e, t, a) {
          return J = "useSyncExternalStore", he(), Sm(e, t);
        },
        useId: function() {
          return J = "useId", he(), Nm();
        },
        unstable_isNewReconciler: I
      }, Cb = {
        readContext: function(e) {
          return ur(e);
        },
        useCallback: function(e, t) {
          return J = "useCallback", he(), _m(e, t);
        },
        useContext: function(e) {
          return J = "useContext", he(), ur(e);
        },
        useEffect: function(e, t) {
          return J = "useEffect", he(), Fp(e, t);
        },
        useImperativeHandle: function(e, t, a) {
          return J = "useImperativeHandle", he(), Tm(e, t, a);
        },
        useInsertionEffect: function(e, t) {
          return J = "useInsertionEffect", he(), wm(e, t);
        },
        useLayoutEffect: function(e, t) {
          return J = "useLayoutEffect", he(), Rm(e, t);
        },
        useMemo: function(e, t) {
          J = "useMemo", he();
          var a = Ee.current;
          Ee.current = Mm;
          try {
            return Dm(e, t);
          } finally {
            Ee.current = a;
          }
        },
        useReducer: function(e, t, a) {
          J = "useReducer", he();
          var i = Ee.current;
          Ee.current = Mm;
          try {
            return Zg(e, t, a);
          } finally {
            Ee.current = i;
          }
        },
        useRef: function(e) {
          return J = "useRef", he(), bm();
        },
        useState: function(e) {
          J = "useState", he();
          var t = Ee.current;
          Ee.current = Mm;
          try {
            return n0(e);
          } finally {
            Ee.current = t;
          }
        },
        useDebugValue: function(e, t) {
          return J = "useDebugValue", he(), km();
        },
        useDeferredValue: function(e) {
          return J = "useDeferredValue", he(), cb(e);
        },
        useTransition: function() {
          return J = "useTransition", he(), pb();
        },
        useMutableSource: function(e, t, a) {
          return J = "useMutableSource", he(), void 0;
        },
        useSyncExternalStore: function(e, t, a) {
          return J = "useSyncExternalStore", he(), Sm(e, t);
        },
        useId: function() {
          return J = "useId", he(), Nm();
        },
        unstable_isNewReconciler: I
      }, Yl = {
        readContext: function(e) {
          return d0(), ur(e);
        },
        useCallback: function(e, t) {
          return J = "useCallback", pt(), en(), o0(e, t);
        },
        useContext: function(e) {
          return J = "useContext", pt(), en(), ur(e);
        },
        useEffect: function(e, t) {
          return J = "useEffect", pt(), en(), Em(e, t);
        },
        useImperativeHandle: function(e, t, a) {
          return J = "useImperativeHandle", pt(), en(), l0(e, t, a);
        },
        useInsertionEffect: function(e, t) {
          return J = "useInsertionEffect", pt(), en(), a0(e, t);
        },
        useLayoutEffect: function(e, t) {
          return J = "useLayoutEffect", pt(), en(), i0(e, t);
        },
        useMemo: function(e, t) {
          J = "useMemo", pt(), en();
          var a = Ee.current;
          Ee.current = Yl;
          try {
            return u0(e, t);
          } finally {
            Ee.current = a;
          }
        },
        useReducer: function(e, t, a) {
          J = "useReducer", pt(), en();
          var i = Ee.current;
          Ee.current = Yl;
          try {
            return Kg(e, t, a);
          } finally {
            Ee.current = i;
          }
        },
        useRef: function(e) {
          return J = "useRef", pt(), en(), r0(e);
        },
        useState: function(e) {
          J = "useState", pt(), en();
          var t = Ee.current;
          Ee.current = Yl;
          try {
            return xm(e);
          } finally {
            Ee.current = t;
          }
        },
        useDebugValue: function(e, t) {
          return J = "useDebugValue", pt(), en(), void 0;
        },
        useDeferredValue: function(e) {
          return J = "useDeferredValue", pt(), en(), s0(e);
        },
        useTransition: function() {
          return J = "useTransition", pt(), en(), c0();
        },
        useMutableSource: function(e, t, a) {
          return J = "useMutableSource", pt(), en(), void 0;
        },
        useSyncExternalStore: function(e, t, a) {
          return J = "useSyncExternalStore", pt(), en(), e0(e, t, a);
        },
        useId: function() {
          return J = "useId", pt(), en(), f0();
        },
        unstable_isNewReconciler: I
      }, ll = {
        readContext: function(e) {
          return d0(), ur(e);
        },
        useCallback: function(e, t) {
          return J = "useCallback", pt(), he(), _m(e, t);
        },
        useContext: function(e) {
          return J = "useContext", pt(), he(), ur(e);
        },
        useEffect: function(e, t) {
          return J = "useEffect", pt(), he(), Fp(e, t);
        },
        useImperativeHandle: function(e, t, a) {
          return J = "useImperativeHandle", pt(), he(), Tm(e, t, a);
        },
        useInsertionEffect: function(e, t) {
          return J = "useInsertionEffect", pt(), he(), wm(e, t);
        },
        useLayoutEffect: function(e, t) {
          return J = "useLayoutEffect", pt(), he(), Rm(e, t);
        },
        useMemo: function(e, t) {
          J = "useMemo", pt(), he();
          var a = Ee.current;
          Ee.current = ll;
          try {
            return Dm(e, t);
          } finally {
            Ee.current = a;
          }
        },
        useReducer: function(e, t, a) {
          J = "useReducer", pt(), he();
          var i = Ee.current;
          Ee.current = ll;
          try {
            return Jg(e, t, a);
          } finally {
            Ee.current = i;
          }
        },
        useRef: function(e) {
          return J = "useRef", pt(), he(), bm();
        },
        useState: function(e) {
          J = "useState", pt(), he();
          var t = Ee.current;
          Ee.current = ll;
          try {
            return t0(e);
          } finally {
            Ee.current = t;
          }
        },
        useDebugValue: function(e, t) {
          return J = "useDebugValue", pt(), he(), km();
        },
        useDeferredValue: function(e) {
          return J = "useDeferredValue", pt(), he(), sb(e);
        },
        useTransition: function() {
          return J = "useTransition", pt(), he(), db();
        },
        useMutableSource: function(e, t, a) {
          return J = "useMutableSource", pt(), he(), void 0;
        },
        useSyncExternalStore: function(e, t, a) {
          return J = "useSyncExternalStore", pt(), he(), Sm(e, t);
        },
        useId: function() {
          return J = "useId", pt(), he(), Nm();
        },
        unstable_isNewReconciler: I
      }, Mm = {
        readContext: function(e) {
          return d0(), ur(e);
        },
        useCallback: function(e, t) {
          return J = "useCallback", pt(), he(), _m(e, t);
        },
        useContext: function(e) {
          return J = "useContext", pt(), he(), ur(e);
        },
        useEffect: function(e, t) {
          return J = "useEffect", pt(), he(), Fp(e, t);
        },
        useImperativeHandle: function(e, t, a) {
          return J = "useImperativeHandle", pt(), he(), Tm(e, t, a);
        },
        useInsertionEffect: function(e, t) {
          return J = "useInsertionEffect", pt(), he(), wm(e, t);
        },
        useLayoutEffect: function(e, t) {
          return J = "useLayoutEffect", pt(), he(), Rm(e, t);
        },
        useMemo: function(e, t) {
          J = "useMemo", pt(), he();
          var a = Ee.current;
          Ee.current = ll;
          try {
            return Dm(e, t);
          } finally {
            Ee.current = a;
          }
        },
        useReducer: function(e, t, a) {
          J = "useReducer", pt(), he();
          var i = Ee.current;
          Ee.current = ll;
          try {
            return Zg(e, t, a);
          } finally {
            Ee.current = i;
          }
        },
        useRef: function(e) {
          return J = "useRef", pt(), he(), bm();
        },
        useState: function(e) {
          J = "useState", pt(), he();
          var t = Ee.current;
          Ee.current = ll;
          try {
            return n0(e);
          } finally {
            Ee.current = t;
          }
        },
        useDebugValue: function(e, t) {
          return J = "useDebugValue", pt(), he(), km();
        },
        useDeferredValue: function(e) {
          return J = "useDeferredValue", pt(), he(), cb(e);
        },
        useTransition: function() {
          return J = "useTransition", pt(), he(), pb();
        },
        useMutableSource: function(e, t, a) {
          return J = "useMutableSource", pt(), he(), void 0;
        },
        useSyncExternalStore: function(e, t, a) {
          return J = "useSyncExternalStore", pt(), he(), Sm(e, t);
        },
        useId: function() {
          return J = "useId", pt(), he(), Nm();
        },
        unstable_isNewReconciler: I
      };
    }
    var Yu = w.unstable_now, Eb = 0, Lm = -1, Hp = -1, jm = -1, p0 = !1, zm = !1;
    function wb() {
      return p0;
    }
    function VR() {
      zm = !0;
    }
    function BR() {
      p0 = !1, zm = !1;
    }
    function $R() {
      p0 = zm, zm = !1;
    }
    function Rb() {
      return Eb;
    }
    function Tb() {
      Eb = Yu();
    }
    function v0(e) {
      Hp = Yu(), e.actualStartTime < 0 && (e.actualStartTime = Yu());
    }
    function kb(e) {
      Hp = -1;
    }
    function Am(e, t) {
      if (Hp >= 0) {
        var a = Yu() - Hp;
        e.actualDuration += a, t && (e.selfBaseDuration = a), Hp = -1;
      }
    }
    function Wl(e) {
      if (Lm >= 0) {
        var t = Yu() - Lm;
        Lm = -1;
        for (var a = e.return; a !== null; ) {
          switch (a.tag) {
            case ne:
              var i = a.stateNode;
              i.effectDuration += t;
              return;
            case ct:
              var o = a.stateNode;
              o.effectDuration += t;
              return;
          }
          a = a.return;
        }
      }
    }
    function h0(e) {
      if (jm >= 0) {
        var t = Yu() - jm;
        jm = -1;
        for (var a = e.return; a !== null; ) {
          switch (a.tag) {
            case ne:
              var i = a.stateNode;
              i !== null && (i.passiveEffectDuration += t);
              return;
            case ct:
              var o = a.stateNode;
              o !== null && (o.passiveEffectDuration += t);
              return;
          }
          a = a.return;
        }
      }
    }
    function Ql() {
      Lm = Yu();
    }
    function m0() {
      jm = Yu();
    }
    function y0(e) {
      for (var t = e.child; t; )
        e.actualDuration += t.actualDuration, t = t.sibling;
    }
    function ol(e, t) {
      if (e && e.defaultProps) {
        var a = Et({}, t), i = e.defaultProps;
        for (var o in i)
          a[o] === void 0 && (a[o] = i[o]);
        return a;
      }
      return t;
    }
    var g0 = {}, S0, x0, b0, C0, E0, _b, Um, w0, R0, T0, Pp;
    {
      S0 = /* @__PURE__ */ new Set(), x0 = /* @__PURE__ */ new Set(), b0 = /* @__PURE__ */ new Set(), C0 = /* @__PURE__ */ new Set(), w0 = /* @__PURE__ */ new Set(), E0 = /* @__PURE__ */ new Set(), R0 = /* @__PURE__ */ new Set(), T0 = /* @__PURE__ */ new Set(), Pp = /* @__PURE__ */ new Set();
      var Db = /* @__PURE__ */ new Set();
      Um = function(e, t) {
        if (!(e === null || typeof e == "function")) {
          var a = t + "_" + e;
          Db.has(a) || (Db.add(a), y("%s(...): Expected the last optional `callback` argument to be a function. Instead received: %s.", t, e));
        }
      }, _b = function(e, t) {
        if (t === void 0) {
          var a = zt(e) || "Component";
          E0.has(a) || (E0.add(a), y("%s.getDerivedStateFromProps(): A valid state object (or null) must be returned. You have returned undefined.", a));
        }
      }, Object.defineProperty(g0, "_processChildContext", {
        enumerable: !1,
        value: function() {
          throw new Error("_processChildContext is not available in React 16+. This likely means you have multiple copies of React and are attempting to nest a React 15 tree inside a React 16 tree using unstable_renderSubtreeIntoContainer, which isn't supported. Try to make sure you have only one copy of React (and ideally, switch to ReactDOM.createPortal).");
        }
      }), Object.freeze(g0);
    }
    function k0(e, t, a, i) {
      var o = e.memoizedState, s = a(i, o);
      {
        if (e.mode & _t) {
          Bn(!0);
          try {
            s = a(i, o);
          } finally {
            Bn(!1);
          }
        }
        _b(t, s);
      }
      var f = s == null ? o : Et({}, o, s);
      if (e.memoizedState = f, e.lanes === Z) {
        var p = e.updateQueue;
        p.baseState = f;
      }
    }
    var _0 = {
      isMounted: wa,
      enqueueSetState: function(e, t, a) {
        var i = Fa(e), o = Na(), s = qu(i), f = Oo(o, s);
        f.payload = t, a != null && (Um(a, "setState"), f.callback = a);
        var p = Vu(i, f, s);
        p !== null && (xr(p, i, s, o), dm(p, i, s)), bs(i, s);
      },
      enqueueReplaceState: function(e, t, a) {
        var i = Fa(e), o = Na(), s = qu(i), f = Oo(o, s);
        f.tag = Wx, f.payload = t, a != null && (Um(a, "replaceState"), f.callback = a);
        var p = Vu(i, f, s);
        p !== null && (xr(p, i, s, o), dm(p, i, s)), bs(i, s);
      },
      enqueueForceUpdate: function(e, t) {
        var a = Fa(e), i = Na(), o = qu(a), s = Oo(i, o);
        s.tag = sm, t != null && (Um(t, "forceUpdate"), s.callback = t);
        var f = Vu(a, s, o);
        f !== null && (xr(f, a, o, i), dm(f, a, o)), Uc(a, o);
      }
    };
    function Nb(e, t, a, i, o, s, f) {
      var p = e.stateNode;
      if (typeof p.shouldComponentUpdate == "function") {
        var v = p.shouldComponentUpdate(i, s, f);
        {
          if (e.mode & _t) {
            Bn(!0);
            try {
              v = p.shouldComponentUpdate(i, s, f);
            } finally {
              Bn(!1);
            }
          }
          v === void 0 && y("%s.shouldComponentUpdate(): Returned undefined instead of a boolean value. Make sure to return true or false.", zt(t) || "Component");
        }
        return v;
      }
      return t.prototype && t.prototype.isPureReactComponent ? !nt(a, i) || !nt(o, s) : !0;
    }
    function IR(e, t, a) {
      var i = e.stateNode;
      {
        var o = zt(t) || "Component", s = i.render;
        s || (t.prototype && typeof t.prototype.render == "function" ? y("%s(...): No `render` method found on the returned component instance: did you accidentally return an object from the constructor?", o) : y("%s(...): No `render` method found on the returned component instance: you may have forgotten to define `render`.", o)), i.getInitialState && !i.getInitialState.isReactClassApproved && !i.state && y("getInitialState was defined on %s, a plain JavaScript class. This is only supported for classes created using React.createClass. Did you mean to define a state property instead?", o), i.getDefaultProps && !i.getDefaultProps.isReactClassApproved && y("getDefaultProps was defined on %s, a plain JavaScript class. This is only supported for classes created using React.createClass. Use a static property to define defaultProps instead.", o), i.propTypes && y("propTypes was defined as an instance property on %s. Use a static property to define propTypes instead.", o), i.contextType && y("contextType was defined as an instance property on %s. Use a static property to define contextType instead.", o), t.childContextTypes && !Pp.has(t) && // Strict Mode has its own warning for legacy context, so we can skip
        // this one.
        (e.mode & _t) === Fe && (Pp.add(t), y(`%s uses the legacy childContextTypes API which is no longer supported and will be removed in the next major release. Use React.createContext() instead

.Learn more about this warning here: https://reactjs.org/link/legacy-context`, o)), t.contextTypes && !Pp.has(t) && // Strict Mode has its own warning for legacy context, so we can skip
        // this one.
        (e.mode & _t) === Fe && (Pp.add(t), y(`%s uses the legacy contextTypes API which is no longer supported and will be removed in the next major release. Use React.createContext() with static contextType instead.

Learn more about this warning here: https://reactjs.org/link/legacy-context`, o)), i.contextTypes && y("contextTypes was defined as an instance property on %s. Use a static property to define contextTypes instead.", o), t.contextType && t.contextTypes && !R0.has(t) && (R0.add(t), y("%s declares both contextTypes and contextType static properties. The legacy contextTypes property will be ignored.", o)), typeof i.componentShouldUpdate == "function" && y("%s has a method called componentShouldUpdate(). Did you mean shouldComponentUpdate()? The name is phrased as a question because the function is expected to return a value.", o), t.prototype && t.prototype.isPureReactComponent && typeof i.shouldComponentUpdate < "u" && y("%s has a method called shouldComponentUpdate(). shouldComponentUpdate should not be used when extending React.PureComponent. Please extend React.Component if shouldComponentUpdate is used.", zt(t) || "A pure component"), typeof i.componentDidUnmount == "function" && y("%s has a method called componentDidUnmount(). But there is no such lifecycle method. Did you mean componentWillUnmount()?", o), typeof i.componentDidReceiveProps == "function" && y("%s has a method called componentDidReceiveProps(). But there is no such lifecycle method. If you meant to update the state in response to changing props, use componentWillReceiveProps(). If you meant to fetch data or run side-effects or mutations after React has updated the UI, use componentDidUpdate().", o), typeof i.componentWillRecieveProps == "function" && y("%s has a method called componentWillRecieveProps(). Did you mean componentWillReceiveProps()?", o), typeof i.UNSAFE_componentWillRecieveProps == "function" && y("%s has a method called UNSAFE_componentWillRecieveProps(). Did you mean UNSAFE_componentWillReceiveProps()?", o);
        var f = i.props !== a;
        i.props !== void 0 && f && y("%s(...): When calling super() in `%s`, make sure to pass up the same props that your component's constructor was passed.", o, o), i.defaultProps && y("Setting defaultProps as an instance property on %s is not supported and will be ignored. Instead, define defaultProps as a static property on %s.", o, o), typeof i.getSnapshotBeforeUpdate == "function" && typeof i.componentDidUpdate != "function" && !b0.has(t) && (b0.add(t), y("%s: getSnapshotBeforeUpdate() should be used with componentDidUpdate(). This component defines getSnapshotBeforeUpdate() only.", zt(t))), typeof i.getDerivedStateFromProps == "function" && y("%s: getDerivedStateFromProps() is defined as an instance method and will be ignored. Instead, declare it as a static method.", o), typeof i.getDerivedStateFromError == "function" && y("%s: getDerivedStateFromError() is defined as an instance method and will be ignored. Instead, declare it as a static method.", o), typeof t.getSnapshotBeforeUpdate == "function" && y("%s: getSnapshotBeforeUpdate() is defined as a static method and will be ignored. Instead, declare it as an instance method.", o);
        var p = i.state;
        p && (typeof p != "object" || At(p)) && y("%s.state: must be set to an object or null", o), typeof i.getChildContext == "function" && typeof t.childContextTypes != "object" && y("%s.getChildContext(): childContextTypes must be defined in order to use getChildContext().", o);
      }
    }
    function Ob(e, t) {
      t.updater = _0, e.stateNode = t, au(t, e), t._reactInternalInstance = g0;
    }
    function Mb(e, t, a) {
      var i = !1, o = pi, s = pi, f = t.contextType;
      if ("contextType" in t) {
        var p = (
          // Allow null for conditional declaration
          f === null || f !== void 0 && f.$$typeof === ee && f._context === void 0
        );
        if (!p && !T0.has(t)) {
          T0.add(t);
          var v = "";
          f === void 0 ? v = " However, it is set to undefined. This can be caused by a typo or by mixing up named and default imports. This can also happen due to a circular dependency, so try moving the createContext() call to a separate file." : typeof f != "object" ? v = " However, it is set to a " + typeof f + "." : f.$$typeof === T ? v = " Did you accidentally pass the Context.Provider instead?" : f._context !== void 0 ? v = " Did you accidentally pass the Context.Consumer instead?" : v = " However, it is set to an object with keys {" + Object.keys(f).join(", ") + "}.", y("%s defines an invalid contextType. contextType should point to the Context object returned by React.createContext().%s", zt(t) || "Component", v);
        }
      }
      if (typeof f == "object" && f !== null)
        s = ur(f);
      else {
        o = Of(e, t, !0);
        var g = t.contextTypes;
        i = g != null, s = i ? Mf(e, o) : pi;
      }
      var x = new t(a, s);
      if (e.mode & _t) {
        Bn(!0);
        try {
          x = new t(a, s);
        } finally {
          Bn(!1);
        }
      }
      var N = e.memoizedState = x.state !== null && x.state !== void 0 ? x.state : null;
      Ob(e, x);
      {
        if (typeof t.getDerivedStateFromProps == "function" && N === null) {
          var _ = zt(t) || "Component";
          x0.has(_) || (x0.add(_), y("`%s` uses `getDerivedStateFromProps` but its initial state is %s. This is not recommended. Instead, define the initial state by assigning an object to `this.state` in the constructor of `%s`. This ensures that `getDerivedStateFromProps` arguments have a consistent shape.", _, x.state === null ? "null" : "undefined", _));
        }
        if (typeof t.getDerivedStateFromProps == "function" || typeof x.getSnapshotBeforeUpdate == "function") {
          var A = null, P = null, Q = null;
          if (typeof x.componentWillMount == "function" && x.componentWillMount.__suppressDeprecationWarning !== !0 ? A = "componentWillMount" : typeof x.UNSAFE_componentWillMount == "function" && (A = "UNSAFE_componentWillMount"), typeof x.componentWillReceiveProps == "function" && x.componentWillReceiveProps.__suppressDeprecationWarning !== !0 ? P = "componentWillReceiveProps" : typeof x.UNSAFE_componentWillReceiveProps == "function" && (P = "UNSAFE_componentWillReceiveProps"), typeof x.componentWillUpdate == "function" && x.componentWillUpdate.__suppressDeprecationWarning !== !0 ? Q = "componentWillUpdate" : typeof x.UNSAFE_componentWillUpdate == "function" && (Q = "UNSAFE_componentWillUpdate"), A !== null || P !== null || Q !== null) {
            var ge = zt(t) || "Component", Xe = typeof t.getDerivedStateFromProps == "function" ? "getDerivedStateFromProps()" : "getSnapshotBeforeUpdate()";
            C0.has(ge) || (C0.add(ge), y(`Unsafe legacy lifecycles will not be called for components using new component APIs.

%s uses %s but also contains the following legacy lifecycles:%s%s%s

The above lifecycles should be removed. Learn more about this warning here:
https://reactjs.org/link/unsafe-component-lifecycles`, ge, Xe, A !== null ? `
  ` + A : "", P !== null ? `
  ` + P : "", Q !== null ? `
  ` + Q : ""));
          }
        }
      }
      return i && bx(e, o, s), x;
    }
    function YR(e, t) {
      var a = t.state;
      typeof t.componentWillMount == "function" && t.componentWillMount(), typeof t.UNSAFE_componentWillMount == "function" && t.UNSAFE_componentWillMount(), a !== t.state && (y("%s.componentWillMount(): Assigning directly to this.state is deprecated (except inside a component's constructor). Use setState instead.", dt(e) || "Component"), _0.enqueueReplaceState(t, t.state, null));
    }
    function Lb(e, t, a, i) {
      var o = t.state;
      if (typeof t.componentWillReceiveProps == "function" && t.componentWillReceiveProps(a, i), typeof t.UNSAFE_componentWillReceiveProps == "function" && t.UNSAFE_componentWillReceiveProps(a, i), t.state !== o) {
        {
          var s = dt(e) || "Component";
          S0.has(s) || (S0.add(s), y("%s.componentWillReceiveProps(): Assigning directly to this.state is deprecated (except inside a component's constructor). Use setState instead.", s));
        }
        _0.enqueueReplaceState(t, t.state, null);
      }
    }
    function D0(e, t, a, i) {
      IR(e, t, a);
      var o = e.stateNode;
      o.props = a, o.state = e.memoizedState, o.refs = {}, Fg(e);
      var s = t.contextType;
      if (typeof s == "object" && s !== null)
        o.context = ur(s);
      else {
        var f = Of(e, t, !0);
        o.context = Mf(e, f);
      }
      {
        if (o.state === a) {
          var p = zt(t) || "Component";
          w0.has(p) || (w0.add(p), y("%s: It is not recommended to assign props directly to state because updates to props won't be reflected in state. In most cases, it is better to use props directly.", p));
        }
        e.mode & _t && al.recordLegacyContextWarning(e, o), al.recordUnsafeLifecycleWarnings(e, o);
      }
      o.state = e.memoizedState;
      var v = t.getDerivedStateFromProps;
      if (typeof v == "function" && (k0(e, t, v, a), o.state = e.memoizedState), typeof t.getDerivedStateFromProps != "function" && typeof o.getSnapshotBeforeUpdate != "function" && (typeof o.UNSAFE_componentWillMount == "function" || typeof o.componentWillMount == "function") && (YR(e, o), pm(e, a, o, i), o.state = e.memoizedState), typeof o.componentDidMount == "function") {
        var g = xt;
        g |= ra, (e.mode & Ta) !== Fe && (g |= aa), e.flags |= g;
      }
    }
    function WR(e, t, a, i) {
      var o = e.stateNode, s = e.memoizedProps;
      o.props = s;
      var f = o.context, p = t.contextType, v = pi;
      if (typeof p == "object" && p !== null)
        v = ur(p);
      else {
        var g = Of(e, t, !0);
        v = Mf(e, g);
      }
      var x = t.getDerivedStateFromProps, N = typeof x == "function" || typeof o.getSnapshotBeforeUpdate == "function";
      !N && (typeof o.UNSAFE_componentWillReceiveProps == "function" || typeof o.componentWillReceiveProps == "function") && (s !== a || f !== v) && Lb(e, o, a, v), Gx();
      var _ = e.memoizedState, A = o.state = _;
      if (pm(e, a, o, i), A = e.memoizedState, s === a && _ === A && !Gh() && !vm()) {
        if (typeof o.componentDidMount == "function") {
          var P = xt;
          P |= ra, (e.mode & Ta) !== Fe && (P |= aa), e.flags |= P;
        }
        return !1;
      }
      typeof x == "function" && (k0(e, t, x, a), A = e.memoizedState);
      var Q = vm() || Nb(e, t, s, a, _, A, v);
      if (Q) {
        if (!N && (typeof o.UNSAFE_componentWillMount == "function" || typeof o.componentWillMount == "function") && (typeof o.componentWillMount == "function" && o.componentWillMount(), typeof o.UNSAFE_componentWillMount == "function" && o.UNSAFE_componentWillMount()), typeof o.componentDidMount == "function") {
          var ge = xt;
          ge |= ra, (e.mode & Ta) !== Fe && (ge |= aa), e.flags |= ge;
        }
      } else {
        if (typeof o.componentDidMount == "function") {
          var Xe = xt;
          Xe |= ra, (e.mode & Ta) !== Fe && (Xe |= aa), e.flags |= Xe;
        }
        e.memoizedProps = a, e.memoizedState = A;
      }
      return o.props = a, o.state = A, o.context = v, Q;
    }
    function QR(e, t, a, i, o) {
      var s = t.stateNode;
      Qx(e, t);
      var f = t.memoizedProps, p = t.type === t.elementType ? f : ol(t.type, f);
      s.props = p;
      var v = t.pendingProps, g = s.context, x = a.contextType, N = pi;
      if (typeof x == "object" && x !== null)
        N = ur(x);
      else {
        var _ = Of(t, a, !0);
        N = Mf(t, _);
      }
      var A = a.getDerivedStateFromProps, P = typeof A == "function" || typeof s.getSnapshotBeforeUpdate == "function";
      !P && (typeof s.UNSAFE_componentWillReceiveProps == "function" || typeof s.componentWillReceiveProps == "function") && (f !== v || g !== N) && Lb(t, s, i, N), Gx();
      var Q = t.memoizedState, ge = s.state = Q;
      if (pm(t, i, s, o), ge = t.memoizedState, f === v && Q === ge && !Gh() && !vm() && !Ue)
        return typeof s.componentDidUpdate == "function" && (f !== e.memoizedProps || Q !== e.memoizedState) && (t.flags |= xt), typeof s.getSnapshotBeforeUpdate == "function" && (f !== e.memoizedProps || Q !== e.memoizedState) && (t.flags |= Ha), !1;
      typeof A == "function" && (k0(t, a, A, i), ge = t.memoizedState);
      var Xe = vm() || Nb(t, a, p, i, Q, ge, N) || // TODO: In some cases, we'll end up checking if context has changed twice,
      // both before and after `shouldComponentUpdate` has been called. Not ideal,
      // but I'm loath to refactor this function. This only happens for memoized
      // components so it's not that common.
      Ue;
      return Xe ? (!P && (typeof s.UNSAFE_componentWillUpdate == "function" || typeof s.componentWillUpdate == "function") && (typeof s.componentWillUpdate == "function" && s.componentWillUpdate(i, ge, N), typeof s.UNSAFE_componentWillUpdate == "function" && s.UNSAFE_componentWillUpdate(i, ge, N)), typeof s.componentDidUpdate == "function" && (t.flags |= xt), typeof s.getSnapshotBeforeUpdate == "function" && (t.flags |= Ha)) : (typeof s.componentDidUpdate == "function" && (f !== e.memoizedProps || Q !== e.memoizedState) && (t.flags |= xt), typeof s.getSnapshotBeforeUpdate == "function" && (f !== e.memoizedProps || Q !== e.memoizedState) && (t.flags |= Ha), t.memoizedProps = i, t.memoizedState = ge), s.props = i, s.state = ge, s.context = N, Xe;
    }
    function Js(e, t) {
      return {
        value: e,
        source: t,
        stack: Yo(t),
        digest: null
      };
    }
    function N0(e, t, a) {
      return {
        value: e,
        source: null,
        stack: a ?? null,
        digest: t ?? null
      };
    }
    function GR(e, t) {
      return !0;
    }
    function O0(e, t) {
      try {
        var a = GR(e, t);
        if (a === !1)
          return;
        var i = t.value, o = t.source, s = t.stack, f = s !== null ? s : "";
        if (i != null && i._suppressLogging) {
          if (e.tag === K)
            return;
          console.error(i);
        }
        var p = o ? dt(o) : null, v = p ? "The above error occurred in the <" + p + "> component:" : "The above error occurred in one of your React components:", g;
        if (e.tag === ne)
          g = `Consider adding an error boundary to your tree to customize error handling behavior.
Visit https://reactjs.org/link/error-boundaries to learn more about error boundaries.`;
        else {
          var x = dt(e) || "Anonymous";
          g = "React will try to recreate this component tree from scratch " + ("using the error boundary you provided, " + x + ".");
        }
        var N = v + `
` + f + `

` + ("" + g);
        console.error(N);
      } catch (_) {
        setTimeout(function() {
          throw _;
        });
      }
    }
    var qR = typeof WeakMap == "function" ? WeakMap : Map;
    function jb(e, t, a) {
      var i = Oo(fn, a);
      i.tag = Ag, i.payload = {
        element: null
      };
      var o = t.value;
      return i.callback = function() {
        Vk(o), O0(e, t);
      }, i;
    }
    function M0(e, t, a) {
      var i = Oo(fn, a);
      i.tag = Ag;
      var o = e.type.getDerivedStateFromError;
      if (typeof o == "function") {
        var s = t.value;
        i.payload = function() {
          return o(s);
        }, i.callback = function() {
          YC(e), O0(e, t);
        };
      }
      var f = e.stateNode;
      return f !== null && typeof f.componentDidCatch == "function" && (i.callback = function() {
        YC(e), O0(e, t), typeof o != "function" && Hk(this);
        var v = t.value, g = t.stack;
        this.componentDidCatch(v, {
          componentStack: g !== null ? g : ""
        }), typeof o != "function" && (ca(e.lanes, Qe) || y("%s: Error boundaries should implement getDerivedStateFromError(). In that method, return a state update to display an error message or fallback UI.", dt(e) || "Unknown"));
      }), i;
    }
    function zb(e, t, a) {
      var i = e.pingCache, o;
      if (i === null ? (i = e.pingCache = new qR(), o = /* @__PURE__ */ new Set(), i.set(t, o)) : (o = i.get(t), o === void 0 && (o = /* @__PURE__ */ new Set(), i.set(t, o))), !o.has(a)) {
        o.add(a);
        var s = Bk.bind(null, e, t, a);
        Ra && rv(e, a), t.then(s, s);
      }
    }
    function XR(e, t, a, i) {
      var o = e.updateQueue;
      if (o === null) {
        var s = /* @__PURE__ */ new Set();
        s.add(a), e.updateQueue = s;
      } else
        o.add(a);
    }
    function KR(e, t) {
      var a = e.tag;
      if ((e.mode & Ve) === Fe && (a === B || a === Ke || a === Ye)) {
        var i = e.alternate;
        i ? (e.updateQueue = i.updateQueue, e.memoizedState = i.memoizedState, e.lanes = i.lanes) : (e.updateQueue = null, e.memoizedState = null);
      }
    }
    function Ab(e) {
      var t = e;
      do {
        if (t.tag === ke && OR(t))
          return t;
        t = t.return;
      } while (t !== null);
      return null;
    }
    function Ub(e, t, a, i, o) {
      if ((e.mode & Ve) === Fe) {
        if (e === t)
          e.flags |= ar;
        else {
          if (e.flags |= ot, a.flags |= gs, a.flags &= ~(Rc | Ca), a.tag === K) {
            var s = a.alternate;
            if (s === null)
              a.tag = Oe;
            else {
              var f = Oo(fn, Qe);
              f.tag = sm, Vu(a, f, Qe);
            }
          }
          a.lanes = gt(a.lanes, Qe);
        }
        return e;
      }
      return e.flags |= ar, e.lanes = o, e;
    }
    function JR(e, t, a, i, o) {
      if (a.flags |= Ca, Ra && rv(e, o), i !== null && typeof i == "object" && typeof i.then == "function") {
        var s = i;
        KR(a), Pr() && a.mode & Ve && _x();
        var f = Ab(t);
        if (f !== null) {
          f.flags &= ~_n, Ub(f, t, a, e, o), f.mode & Ve && zb(e, s, o), XR(f, e, s);
          return;
        } else {
          if (!$d(o)) {
            zb(e, s, o), fS();
            return;
          }
          var p = new Error("A component suspended while responding to synchronous input. This will cause the UI to be replaced with a loading indicator. To fix, updates that suspend should be wrapped with startTransition.");
          i = p;
        }
      } else if (Pr() && a.mode & Ve) {
        _x();
        var v = Ab(t);
        if (v !== null) {
          (v.flags & ar) === qe && (v.flags |= _n), Ub(v, t, a, e, o), wg(Js(i, a));
          return;
        }
      }
      i = Js(i, a), Ok(i);
      var g = t;
      do {
        switch (g.tag) {
          case ne: {
            var x = i;
            g.flags |= ar;
            var N = gu(o);
            g.lanes = gt(g.lanes, N);
            var _ = jb(g, x, N);
            Hg(g, _);
            return;
          }
          case K:
            var A = i, P = g.type, Q = g.stateNode;
            if ((g.flags & ot) === qe && (typeof P.getDerivedStateFromError == "function" || Q !== null && typeof Q.componentDidCatch == "function" && !AC(Q))) {
              g.flags |= ar;
              var ge = gu(o);
              g.lanes = gt(g.lanes, ge);
              var Xe = M0(g, A, ge);
              Hg(g, Xe);
              return;
            }
            break;
        }
        g = g.return;
      } while (g !== null);
    }
    function ZR() {
      return null;
    }
    var Vp = b.ReactCurrentOwner, ul = !1, L0, Bp, j0, z0, A0, Zs, U0, Fm, $p;
    L0 = {}, Bp = {}, j0 = {}, z0 = {}, A0 = {}, Zs = !1, U0 = {}, Fm = {}, $p = {};
    function _a(e, t, a, i) {
      e === null ? t.child = Px(t, null, a, i) : t.child = Af(t, e.child, a, i);
    }
    function eT(e, t, a, i) {
      t.child = Af(t, e.child, null, i), t.child = Af(t, null, a, i);
    }
    function Fb(e, t, a, i, o) {
      if (t.type !== t.elementType) {
        var s = a.propTypes;
        s && nl(
          s,
          i,
          // Resolved props
          "prop",
          zt(a)
        );
      }
      var f = a.render, p = t.ref, v, g;
      Ff(t, o), uu(t);
      {
        if (Vp.current = t, ea(!0), v = If(e, t, f, i, p, o), g = Yf(), t.mode & _t) {
          Bn(!0);
          try {
            v = If(e, t, f, i, p, o), g = Yf();
          } finally {
            Bn(!1);
          }
        }
        ea(!1);
      }
      return oa(), e !== null && !ul ? (eb(e, t, o), Mo(e, t, o)) : (Pr() && g && gg(t), t.flags |= Dl, _a(e, t, v, o), t.child);
    }
    function Hb(e, t, a, i, o) {
      if (e === null) {
        var s = a.type;
        if (i_(s) && a.compare === null && // SimpleMemoComponent codepath doesn't resolve outer props either.
        a.defaultProps === void 0) {
          var f = s;
          return f = Zf(s), t.tag = Ye, t.type = f, P0(t, s), Pb(e, t, f, i, o);
        }
        {
          var p = s.propTypes;
          if (p && nl(
            p,
            i,
            // Resolved props
            "prop",
            zt(s)
          ), a.defaultProps !== void 0) {
            var v = zt(s) || "Unknown";
            $p[v] || (y("%s: Support for defaultProps will be removed from memo components in a future major release. Use JavaScript default parameters instead.", v), $p[v] = !0);
          }
        }
        var g = CS(a.type, null, i, t, t.mode, o);
        return g.ref = t.ref, g.return = t, t.child = g, g;
      }
      {
        var x = a.type, N = x.propTypes;
        N && nl(
          N,
          i,
          // Resolved props
          "prop",
          zt(x)
        );
      }
      var _ = e.child, A = W0(e, o);
      if (!A) {
        var P = _.memoizedProps, Q = a.compare;
        if (Q = Q !== null ? Q : nt, Q(P, i) && e.ref === t.ref)
          return Mo(e, t, o);
      }
      t.flags |= Dl;
      var ge = ac(_, i);
      return ge.ref = t.ref, ge.return = t, t.child = ge, ge;
    }
    function Pb(e, t, a, i, o) {
      if (t.type !== t.elementType) {
        var s = t.elementType;
        if (s.$$typeof === Ze) {
          var f = s, p = f._payload, v = f._init;
          try {
            s = v(p);
          } catch {
            s = null;
          }
          var g = s && s.propTypes;
          g && nl(
            g,
            i,
            // Resolved (SimpleMemoComponent has no defaultProps)
            "prop",
            zt(s)
          );
        }
      }
      if (e !== null) {
        var x = e.memoizedProps;
        if (nt(x, i) && e.ref === t.ref && // Prevent bailout if the implementation changed due to hot reload.
        t.type === e.type)
          if (ul = !1, t.pendingProps = i = x, W0(e, o))
            (e.flags & gs) !== qe && (ul = !0);
          else
            return t.lanes = e.lanes, Mo(e, t, o);
      }
      return F0(e, t, a, i, o);
    }
    function Vb(e, t, a) {
      var i = t.pendingProps, o = i.children, s = e !== null ? e.memoizedState : null;
      if (i.mode === "hidden" || pe)
        if ((t.mode & Ve) === Fe) {
          var f = {
            baseLanes: Z,
            cachePool: null,
            transitions: null
          };
          t.memoizedState = f, Km(t, a);
        } else if (ca(a, _r)) {
          var N = {
            baseLanes: Z,
            cachePool: null,
            transitions: null
          };
          t.memoizedState = N;
          var _ = s !== null ? s.baseLanes : a;
          Km(t, _);
        } else {
          var p = null, v;
          if (s !== null) {
            var g = s.baseLanes;
            v = gt(g, a);
          } else
            v = a;
          t.lanes = t.childLanes = _r;
          var x = {
            baseLanes: v,
            cachePool: p,
            transitions: null
          };
          return t.memoizedState = x, t.updateQueue = null, Km(t, v), null;
        }
      else {
        var A;
        s !== null ? (A = gt(s.baseLanes, a), t.memoizedState = null) : A = a, Km(t, A);
      }
      return _a(e, t, o, a), t.child;
    }
    function tT(e, t, a) {
      var i = t.pendingProps;
      return _a(e, t, i, a), t.child;
    }
    function nT(e, t, a) {
      var i = t.pendingProps.children;
      return _a(e, t, i, a), t.child;
    }
    function rT(e, t, a) {
      {
        t.flags |= xt;
        {
          var i = t.stateNode;
          i.effectDuration = 0, i.passiveEffectDuration = 0;
        }
      }
      var o = t.pendingProps, s = o.children;
      return _a(e, t, s, a), t.child;
    }
    function Bb(e, t) {
      var a = t.ref;
      (e === null && a !== null || e !== null && e.ref !== a) && (t.flags |= na, t.flags |= Nd);
    }
    function F0(e, t, a, i, o) {
      if (t.type !== t.elementType) {
        var s = a.propTypes;
        s && nl(
          s,
          i,
          // Resolved props
          "prop",
          zt(a)
        );
      }
      var f;
      {
        var p = Of(t, a, !0);
        f = Mf(t, p);
      }
      var v, g;
      Ff(t, o), uu(t);
      {
        if (Vp.current = t, ea(!0), v = If(e, t, a, i, f, o), g = Yf(), t.mode & _t) {
          Bn(!0);
          try {
            v = If(e, t, a, i, f, o), g = Yf();
          } finally {
            Bn(!1);
          }
        }
        ea(!1);
      }
      return oa(), e !== null && !ul ? (eb(e, t, o), Mo(e, t, o)) : (Pr() && g && gg(t), t.flags |= Dl, _a(e, t, v, o), t.child);
    }
    function $b(e, t, a, i, o) {
      {
        switch (x_(t)) {
          case !1: {
            var s = t.stateNode, f = t.type, p = new f(t.memoizedProps, s.context), v = p.state;
            s.updater.enqueueSetState(s, v, null);
            break;
          }
          case !0: {
            t.flags |= ot, t.flags |= ar;
            var g = new Error("Simulated error coming from DevTools"), x = gu(o);
            t.lanes = gt(t.lanes, x);
            var N = M0(t, Js(g, t), x);
            Hg(t, N);
            break;
          }
        }
        if (t.type !== t.elementType) {
          var _ = a.propTypes;
          _ && nl(
            _,
            i,
            // Resolved props
            "prop",
            zt(a)
          );
        }
      }
      var A;
      Bl(a) ? (A = !0, Xh(t)) : A = !1, Ff(t, o);
      var P = t.stateNode, Q;
      P === null ? (Pm(e, t), Mb(t, a, i), D0(t, a, i, o), Q = !0) : e === null ? Q = WR(t, a, i, o) : Q = QR(e, t, a, i, o);
      var ge = H0(e, t, a, Q, A, o);
      {
        var Xe = t.stateNode;
        Q && Xe.props !== i && (Zs || y("It looks like %s is reassigning its own `this.props` while rendering. This is not supported and can lead to confusing bugs.", dt(t) || "a component"), Zs = !0);
      }
      return ge;
    }
    function H0(e, t, a, i, o, s) {
      Bb(e, t);
      var f = (t.flags & ot) !== qe;
      if (!i && !f)
        return o && wx(t, a, !1), Mo(e, t, s);
      var p = t.stateNode;
      Vp.current = t;
      var v;
      if (f && typeof a.getDerivedStateFromError != "function")
        v = null, kb();
      else {
        uu(t);
        {
          if (ea(!0), v = p.render(), t.mode & _t) {
            Bn(!0);
            try {
              p.render();
            } finally {
              Bn(!1);
            }
          }
          ea(!1);
        }
        oa();
      }
      return t.flags |= Dl, e !== null && f ? eT(e, t, v, s) : _a(e, t, v, s), t.memoizedState = p.state, o && wx(t, a, !0), t.child;
    }
    function Ib(e) {
      var t = e.stateNode;
      t.pendingContext ? Cx(e, t.pendingContext, t.pendingContext !== t.context) : t.context && Cx(e, t.context, !1), Pg(e, t.containerInfo);
    }
    function aT(e, t, a) {
      if (Ib(t), e === null)
        throw new Error("Should have a current fiber. This is a bug in React.");
      var i = t.pendingProps, o = t.memoizedState, s = o.element;
      Qx(e, t), pm(t, i, null, a);
      var f = t.memoizedState;
      t.stateNode;
      var p = f.element;
      if (o.isDehydrated) {
        var v = {
          element: p,
          isDehydrated: !1,
          cache: f.cache,
          pendingSuspenseBoundaries: f.pendingSuspenseBoundaries,
          transitions: f.transitions
        }, g = t.updateQueue;
        if (g.baseState = v, t.memoizedState = v, t.flags & _n) {
          var x = Js(new Error("There was an error while hydrating. Because the error happened outside of a Suspense boundary, the entire root will switch to client rendering."), t);
          return Yb(e, t, p, a, x);
        } else if (p !== s) {
          var N = Js(new Error("This root received an early update, before anything was able hydrate. Switched the entire root to client rendering."), t);
          return Yb(e, t, p, a, N);
        } else {
          oR(t);
          var _ = Px(t, null, p, a);
          t.child = _;
          for (var A = _; A; )
            A.flags = A.flags & ~pn | Pa, A = A.sibling;
        }
      } else {
        if (zf(), p === s)
          return Mo(e, t, a);
        _a(e, t, p, a);
      }
      return t.child;
    }
    function Yb(e, t, a, i, o) {
      return zf(), wg(o), t.flags |= _n, _a(e, t, a, i), t.child;
    }
    function iT(e, t, a) {
      Kx(t), e === null && Eg(t);
      var i = t.type, o = t.pendingProps, s = e !== null ? e.memoizedProps : null, f = o.children, p = ag(i, o);
      return p ? f = null : s !== null && ag(i, s) && (t.flags |= Zt), Bb(e, t), _a(e, t, f, a), t.child;
    }
    function lT(e, t) {
      return e === null && Eg(t), null;
    }
    function oT(e, t, a, i) {
      Pm(e, t);
      var o = t.pendingProps, s = a, f = s._payload, p = s._init, v = p(f);
      t.type = v;
      var g = t.tag = l_(v), x = ol(v, o), N;
      switch (g) {
        case B:
          return P0(t, v), t.type = v = Zf(v), N = F0(null, t, v, x, i), N;
        case K:
          return t.type = v = mS(v), N = $b(null, t, v, x, i), N;
        case Ke:
          return t.type = v = yS(v), N = Fb(null, t, v, x, i), N;
        case at: {
          if (t.type !== t.elementType) {
            var _ = v.propTypes;
            _ && nl(
              _,
              x,
              // Resolved for outer only
              "prop",
              zt(v)
            );
          }
          return N = Hb(
            null,
            t,
            v,
            ol(v.type, x),
            // The inner type can have defaults too
            i
          ), N;
        }
      }
      var A = "";
      throw v !== null && typeof v == "object" && v.$$typeof === Ze && (A = " Did you wrap a component in React.lazy() more than once?"), new Error("Element type is invalid. Received a promise that resolves to: " + v + ". " + ("Lazy element type must resolve to a class or function." + A));
    }
    function uT(e, t, a, i, o) {
      Pm(e, t), t.tag = K;
      var s;
      return Bl(a) ? (s = !0, Xh(t)) : s = !1, Ff(t, o), Mb(t, a, i), D0(t, a, i, o), H0(null, t, a, !0, s, o);
    }
    function sT(e, t, a, i) {
      Pm(e, t);
      var o = t.pendingProps, s;
      {
        var f = Of(t, a, !1);
        s = Mf(t, f);
      }
      Ff(t, i);
      var p, v;
      uu(t);
      {
        if (a.prototype && typeof a.prototype.render == "function") {
          var g = zt(a) || "Unknown";
          L0[g] || (y("The <%s /> component appears to have a render method, but doesn't extend React.Component. This is likely to cause errors. Change %s to extend React.Component instead.", g, g), L0[g] = !0);
        }
        t.mode & _t && al.recordLegacyContextWarning(t, null), ea(!0), Vp.current = t, p = If(null, t, a, o, s, i), v = Yf(), ea(!1);
      }
      if (oa(), t.flags |= Dl, typeof p == "object" && p !== null && typeof p.render == "function" && p.$$typeof === void 0) {
        var x = zt(a) || "Unknown";
        Bp[x] || (y("The <%s /> component appears to be a function component that returns a class instance. Change %s to a class that extends React.Component instead. If you can't use a class try assigning the prototype on the function as a workaround. `%s.prototype = React.Component.prototype`. Don't use an arrow function since it cannot be called with `new` by React.", x, x, x), Bp[x] = !0);
      }
      if (
        // Run these checks in production only if the flag is off.
        // Eventually we'll delete this branch altogether.
        typeof p == "object" && p !== null && typeof p.render == "function" && p.$$typeof === void 0
      ) {
        {
          var N = zt(a) || "Unknown";
          Bp[N] || (y("The <%s /> component appears to be a function component that returns a class instance. Change %s to a class that extends React.Component instead. If you can't use a class try assigning the prototype on the function as a workaround. `%s.prototype = React.Component.prototype`. Don't use an arrow function since it cannot be called with `new` by React.", N, N, N), Bp[N] = !0);
        }
        t.tag = K, t.memoizedState = null, t.updateQueue = null;
        var _ = !1;
        return Bl(a) ? (_ = !0, Xh(t)) : _ = !1, t.memoizedState = p.state !== null && p.state !== void 0 ? p.state : null, Fg(t), Ob(t, p), D0(t, a, o, i), H0(null, t, a, !0, _, i);
      } else {
        if (t.tag = B, t.mode & _t) {
          Bn(!0);
          try {
            p = If(null, t, a, o, s, i), v = Yf();
          } finally {
            Bn(!1);
          }
        }
        return Pr() && v && gg(t), _a(null, t, p, i), P0(t, a), t.child;
      }
    }
    function P0(e, t) {
      {
        if (t && t.childContextTypes && y("%s(...): childContextTypes cannot be defined on a function component.", t.displayName || t.name || "Component"), e.ref !== null) {
          var a = "", i = Ur();
          i && (a += `

Check the render method of \`` + i + "`.");
          var o = i || "", s = e._debugSource;
          s && (o = s.fileName + ":" + s.lineNumber), A0[o] || (A0[o] = !0, y("Function components cannot be given refs. Attempts to access this ref will fail. Did you mean to use React.forwardRef()?%s", a));
        }
        if (t.defaultProps !== void 0) {
          var f = zt(t) || "Unknown";
          $p[f] || (y("%s: Support for defaultProps will be removed from function components in a future major release. Use JavaScript default parameters instead.", f), $p[f] = !0);
        }
        if (typeof t.getDerivedStateFromProps == "function") {
          var p = zt(t) || "Unknown";
          z0[p] || (y("%s: Function components do not support getDerivedStateFromProps.", p), z0[p] = !0);
        }
        if (typeof t.contextType == "object" && t.contextType !== null) {
          var v = zt(t) || "Unknown";
          j0[v] || (y("%s: Function components do not support contextType.", v), j0[v] = !0);
        }
      }
    }
    var V0 = {
      dehydrated: null,
      treeContext: null,
      retryLane: $n
    };
    function B0(e) {
      return {
        baseLanes: e,
        cachePool: ZR(),
        transitions: null
      };
    }
    function cT(e, t) {
      var a = null;
      return {
        baseLanes: gt(e.baseLanes, t),
        cachePool: a,
        transitions: e.transitions
      };
    }
    function fT(e, t, a, i) {
      if (t !== null) {
        var o = t.memoizedState;
        if (o === null)
          return !1;
      }
      return $g(e, Mp);
    }
    function dT(e, t) {
      return _s(e.childLanes, t);
    }
    function Wb(e, t, a) {
      var i = t.pendingProps;
      b_(t) && (t.flags |= ot);
      var o = il.current, s = !1, f = (t.flags & ot) !== qe;
      if (f || fT(o, e) ? (s = !0, t.flags &= ~ot) : (e === null || e.memoizedState !== null) && (o = NR(o, Zx)), o = Pf(o), $u(t, o), e === null) {
        Eg(t);
        var p = t.memoizedState;
        if (p !== null) {
          var v = p.dehydrated;
          if (v !== null)
            return yT(t, v);
        }
        var g = i.children, x = i.fallback;
        if (s) {
          var N = pT(t, g, x, a), _ = t.child;
          return _.memoizedState = B0(a), t.memoizedState = V0, N;
        } else
          return $0(t, g);
      } else {
        var A = e.memoizedState;
        if (A !== null) {
          var P = A.dehydrated;
          if (P !== null)
            return gT(e, t, f, i, P, A, a);
        }
        if (s) {
          var Q = i.fallback, ge = i.children, Xe = hT(e, t, ge, Q, a), Be = t.child, Ht = e.child.memoizedState;
          return Be.memoizedState = Ht === null ? B0(a) : cT(Ht, a), Be.childLanes = dT(e, a), t.memoizedState = V0, Xe;
        } else {
          var Mt = i.children, L = vT(e, t, Mt, a);
          return t.memoizedState = null, L;
        }
      }
    }
    function $0(e, t, a) {
      var i = e.mode, o = {
        mode: "visible",
        children: t
      }, s = I0(o, i);
      return s.return = e, e.child = s, s;
    }
    function pT(e, t, a, i) {
      var o = e.mode, s = e.child, f = {
        mode: "hidden",
        children: t
      }, p, v;
      return (o & Ve) === Fe && s !== null ? (p = s, p.childLanes = Z, p.pendingProps = f, e.mode & ut && (p.actualDuration = 0, p.actualStartTime = -1, p.selfBaseDuration = 0, p.treeBaseDuration = 0), v = Ku(a, o, i, null)) : (p = I0(f, o), v = Ku(a, o, i, null)), p.return = e, v.return = e, p.sibling = v, e.child = p, v;
    }
    function I0(e, t, a) {
      return QC(e, t, Z, null);
    }
    function Qb(e, t) {
      return ac(e, t);
    }
    function vT(e, t, a, i) {
      var o = e.child, s = o.sibling, f = Qb(o, {
        mode: "visible",
        children: a
      });
      if ((t.mode & Ve) === Fe && (f.lanes = i), f.return = t, f.sibling = null, s !== null) {
        var p = t.deletions;
        p === null ? (t.deletions = [s], t.flags |= Gt) : p.push(s);
      }
      return t.child = f, f;
    }
    function hT(e, t, a, i, o) {
      var s = t.mode, f = e.child, p = f.sibling, v = {
        mode: "hidden",
        children: a
      }, g;
      if (
        // In legacy mode, we commit the primary tree as if it successfully
        // completed, even though it's in an inconsistent state.
        (s & Ve) === Fe && // Make sure we're on the second pass, i.e. the primary child fragment was
        // already cloned. In legacy mode, the only case where this isn't true is
        // when DevTools forces us to display a fallback; we skip the first render
        // pass entirely and go straight to rendering the fallback. (In Concurrent
        // Mode, SuspenseList can also trigger this scenario, but this is a legacy-
        // only codepath.)
        t.child !== f
      ) {
        var x = t.child;
        g = x, g.childLanes = Z, g.pendingProps = v, t.mode & ut && (g.actualDuration = 0, g.actualStartTime = -1, g.selfBaseDuration = f.selfBaseDuration, g.treeBaseDuration = f.treeBaseDuration), t.deletions = null;
      } else
        g = Qb(f, v), g.subtreeFlags = f.subtreeFlags & cr;
      var N;
      return p !== null ? N = ac(p, i) : (N = Ku(i, s, o, null), N.flags |= pn), N.return = t, g.return = t, g.sibling = N, t.child = g, N;
    }
    function Hm(e, t, a, i) {
      i !== null && wg(i), Af(t, e.child, null, a);
      var o = t.pendingProps, s = o.children, f = $0(t, s);
      return f.flags |= pn, t.memoizedState = null, f;
    }
    function mT(e, t, a, i, o) {
      var s = t.mode, f = {
        mode: "visible",
        children: a
      }, p = I0(f, s), v = Ku(i, s, o, null);
      return v.flags |= pn, p.return = t, v.return = t, p.sibling = v, t.child = p, (t.mode & Ve) !== Fe && Af(t, e.child, null, o), v;
    }
    function yT(e, t, a) {
      return (e.mode & Ve) === Fe ? (y("Cannot hydrate Suspense in legacy mode. Switch from ReactDOM.hydrate(element, container) to ReactDOMClient.hydrateRoot(container, <App />).render(element) or remove the Suspense components from the server rendered components."), e.lanes = Qe) : ug(t) ? e.lanes = Ki : e.lanes = _r, null;
    }
    function gT(e, t, a, i, o, s, f) {
      if (a)
        if (t.flags & _n) {
          t.flags &= ~_n;
          var L = N0(new Error("There was an error while hydrating this Suspense boundary. Switched to client rendering."));
          return Hm(e, t, f, L);
        } else {
          if (t.memoizedState !== null)
            return t.child = e.child, t.flags |= ot, null;
          var G = i.children, j = i.fallback, le = mT(e, t, G, j, f), we = t.child;
          return we.memoizedState = B0(f), t.memoizedState = V0, le;
        }
      else {
        if (iR(), (t.mode & Ve) === Fe)
          return Hm(
            e,
            t,
            f,
            // TODO: When we delete legacy mode, we should make this error argument
            // required — every concurrent mode path that causes hydration to
            // de-opt to client rendering should have an error message.
            null
          );
        if (ug(o)) {
          var p, v, g;
          {
            var x = Cw(o);
            p = x.digest, v = x.message, g = x.stack;
          }
          var N;
          v ? N = new Error(v) : N = new Error("The server could not finish this Suspense boundary, likely due to an error during server rendering. Switched to client rendering.");
          var _ = N0(N, p, g);
          return Hm(e, t, f, _);
        }
        var A = ca(f, e.childLanes);
        if (ul || A) {
          var P = Xm();
          if (P !== null) {
            var Q = fh(P, f);
            if (Q !== $n && Q !== s.retryLane) {
              s.retryLane = Q;
              var ge = fn;
              Ja(e, Q), xr(P, e, Q, ge);
            }
          }
          fS();
          var Xe = N0(new Error("This Suspense boundary received an update before it finished hydrating. This caused the boundary to switch to client rendering. The usual way to fix this is to wrap the original update in startTransition."));
          return Hm(e, t, f, Xe);
        } else if (mx(o)) {
          t.flags |= ot, t.child = e.child;
          var Be = $k.bind(null, e);
          return Ew(o, Be), null;
        } else {
          uR(t, o, s.treeContext);
          var Ht = i.children, Mt = $0(t, Ht);
          return Mt.flags |= Pa, Mt;
        }
      }
    }
    function Gb(e, t, a) {
      e.lanes = gt(e.lanes, t);
      var i = e.alternate;
      i !== null && (i.lanes = gt(i.lanes, t)), jg(e.return, t, a);
    }
    function ST(e, t, a) {
      for (var i = t; i !== null; ) {
        if (i.tag === ke) {
          var o = i.memoizedState;
          o !== null && Gb(i, a, e);
        } else if (i.tag === it)
          Gb(i, a, e);
        else if (i.child !== null) {
          i.child.return = i, i = i.child;
          continue;
        }
        if (i === e)
          return;
        for (; i.sibling === null; ) {
          if (i.return === null || i.return === e)
            return;
          i = i.return;
        }
        i.sibling.return = i.return, i = i.sibling;
      }
    }
    function xT(e) {
      for (var t = e, a = null; t !== null; ) {
        var i = t.alternate;
        i !== null && ym(i) === null && (a = t), t = t.sibling;
      }
      return a;
    }
    function bT(e) {
      if (e !== void 0 && e !== "forwards" && e !== "backwards" && e !== "together" && !U0[e])
        if (U0[e] = !0, typeof e == "string")
          switch (e.toLowerCase()) {
            case "together":
            case "forwards":
            case "backwards": {
              y('"%s" is not a valid value for revealOrder on <SuspenseList />. Use lowercase "%s" instead.', e, e.toLowerCase());
              break;
            }
            case "forward":
            case "backward": {
              y('"%s" is not a valid value for revealOrder on <SuspenseList />. React uses the -s suffix in the spelling. Use "%ss" instead.', e, e.toLowerCase());
              break;
            }
            default:
              y('"%s" is not a supported revealOrder on <SuspenseList />. Did you mean "together", "forwards" or "backwards"?', e);
              break;
          }
        else
          y('%s is not a supported value for revealOrder on <SuspenseList />. Did you mean "together", "forwards" or "backwards"?', e);
    }
    function CT(e, t) {
      e !== void 0 && !Fm[e] && (e !== "collapsed" && e !== "hidden" ? (Fm[e] = !0, y('"%s" is not a supported value for tail on <SuspenseList />. Did you mean "collapsed" or "hidden"?', e)) : t !== "forwards" && t !== "backwards" && (Fm[e] = !0, y('<SuspenseList tail="%s" /> is only valid if revealOrder is "forwards" or "backwards". Did you mean to specify revealOrder="forwards"?', e)));
    }
    function qb(e, t) {
      {
        var a = At(e), i = !a && typeof jr(e) == "function";
        if (a || i) {
          var o = a ? "array" : "iterable";
          return y("A nested %s was passed to row #%s in <SuspenseList />. Wrap it in an additional SuspenseList to configure its revealOrder: <SuspenseList revealOrder=...> ... <SuspenseList revealOrder=...>{%s}</SuspenseList> ... </SuspenseList>", o, t, o), !1;
        }
      }
      return !0;
    }
    function ET(e, t) {
      if ((t === "forwards" || t === "backwards") && e !== void 0 && e !== null && e !== !1)
        if (At(e)) {
          for (var a = 0; a < e.length; a++)
            if (!qb(e[a], a))
              return;
        } else {
          var i = jr(e);
          if (typeof i == "function") {
            var o = i.call(e);
            if (o)
              for (var s = o.next(), f = 0; !s.done; s = o.next()) {
                if (!qb(s.value, f))
                  return;
                f++;
              }
          } else
            y('A single row was passed to a <SuspenseList revealOrder="%s" />. This is not useful since it needs multiple rows. Did you mean to pass multiple children or an array?', t);
        }
    }
    function Y0(e, t, a, i, o) {
      var s = e.memoizedState;
      s === null ? e.memoizedState = {
        isBackwards: t,
        rendering: null,
        renderingStartTime: 0,
        last: i,
        tail: a,
        tailMode: o
      } : (s.isBackwards = t, s.rendering = null, s.renderingStartTime = 0, s.last = i, s.tail = a, s.tailMode = o);
    }
    function Xb(e, t, a) {
      var i = t.pendingProps, o = i.revealOrder, s = i.tail, f = i.children;
      bT(o), CT(s, o), ET(f, o), _a(e, t, f, a);
      var p = il.current, v = $g(p, Mp);
      if (v)
        p = Ig(p, Mp), t.flags |= ot;
      else {
        var g = e !== null && (e.flags & ot) !== qe;
        g && ST(t, t.child, a), p = Pf(p);
      }
      if ($u(t, p), (t.mode & Ve) === Fe)
        t.memoizedState = null;
      else
        switch (o) {
          case "forwards": {
            var x = xT(t.child), N;
            x === null ? (N = t.child, t.child = null) : (N = x.sibling, x.sibling = null), Y0(
              t,
              !1,
              // isBackwards
              N,
              x,
              s
            );
            break;
          }
          case "backwards": {
            var _ = null, A = t.child;
            for (t.child = null; A !== null; ) {
              var P = A.alternate;
              if (P !== null && ym(P) === null) {
                t.child = A;
                break;
              }
              var Q = A.sibling;
              A.sibling = _, _ = A, A = Q;
            }
            Y0(
              t,
              !0,
              // isBackwards
              _,
              null,
              // last
              s
            );
            break;
          }
          case "together": {
            Y0(
              t,
              !1,
              // isBackwards
              null,
              // tail
              null,
              // last
              void 0
            );
            break;
          }
          default:
            t.memoizedState = null;
        }
      return t.child;
    }
    function wT(e, t, a) {
      Pg(t, t.stateNode.containerInfo);
      var i = t.pendingProps;
      return e === null ? t.child = Af(t, null, i, a) : _a(e, t, i, a), t.child;
    }
    var Kb = !1;
    function RT(e, t, a) {
      var i = t.type, o = i._context, s = t.pendingProps, f = t.memoizedProps, p = s.value;
      {
        "value" in s || Kb || (Kb = !0, y("The `value` prop is required for the `<Context.Provider>`. Did you misspell it or forget to pass it?"));
        var v = t.type.propTypes;
        v && nl(v, s, "prop", "Context.Provider");
      }
      if ($x(t, o, p), f !== null) {
        var g = f.value;
        if (De(g, p)) {
          if (f.children === s.children && !Gh())
            return Mo(e, t, a);
        } else
          bR(t, o, a);
      }
      var x = s.children;
      return _a(e, t, x, a), t.child;
    }
    var Jb = !1;
    function TT(e, t, a) {
      var i = t.type;
      i._context === void 0 ? i !== i.Consumer && (Jb || (Jb = !0, y("Rendering <Context> directly is not supported and will be removed in a future major release. Did you mean to render <Context.Consumer> instead?"))) : i = i._context;
      var o = t.pendingProps, s = o.children;
      typeof s != "function" && y("A context consumer was rendered with multiple children, or a child that isn't a function. A context consumer expects a single child that is a function. If you did pass a function, make sure there is no trailing or leading whitespace around it."), Ff(t, a);
      var f = ur(i);
      uu(t);
      var p;
      return Vp.current = t, ea(!0), p = s(f), ea(!1), oa(), t.flags |= Dl, _a(e, t, p, a), t.child;
    }
    function Ip() {
      ul = !0;
    }
    function Pm(e, t) {
      (t.mode & Ve) === Fe && e !== null && (e.alternate = null, t.alternate = null, t.flags |= pn);
    }
    function Mo(e, t, a) {
      return e !== null && (t.dependencies = e.dependencies), kb(), nv(t.lanes), ca(a, t.childLanes) ? (SR(e, t), t.child) : null;
    }
    function kT(e, t, a) {
      {
        var i = t.return;
        if (i === null)
          throw new Error("Cannot swap the root fiber.");
        if (e.alternate = null, t.alternate = null, a.index = t.index, a.sibling = t.sibling, a.return = t.return, a.ref = t.ref, t === i.child)
          i.child = a;
        else {
          var o = i.child;
          if (o === null)
            throw new Error("Expected parent to have a child.");
          for (; o.sibling !== t; )
            if (o = o.sibling, o === null)
              throw new Error("Expected to find the previous sibling.");
          o.sibling = a;
        }
        var s = i.deletions;
        return s === null ? (i.deletions = [e], i.flags |= Gt) : s.push(e), a.flags |= pn, a;
      }
    }
    function W0(e, t) {
      var a = e.lanes;
      return !!ca(a, t);
    }
    function _T(e, t, a) {
      switch (t.tag) {
        case ne:
          Ib(t), t.stateNode, zf();
          break;
        case V:
          Kx(t);
          break;
        case K: {
          var i = t.type;
          Bl(i) && Xh(t);
          break;
        }
        case oe:
          Pg(t, t.stateNode.containerInfo);
          break;
        case rt: {
          var o = t.memoizedProps.value, s = t.type._context;
          $x(t, s, o);
          break;
        }
        case ct:
          {
            var f = ca(a, t.childLanes);
            f && (t.flags |= xt);
            {
              var p = t.stateNode;
              p.effectDuration = 0, p.passiveEffectDuration = 0;
            }
          }
          break;
        case ke: {
          var v = t.memoizedState;
          if (v !== null) {
            if (v.dehydrated !== null)
              return $u(t, Pf(il.current)), t.flags |= ot, null;
            var g = t.child, x = g.childLanes;
            if (ca(a, x))
              return Wb(e, t, a);
            $u(t, Pf(il.current));
            var N = Mo(e, t, a);
            return N !== null ? N.sibling : null;
          } else
            $u(t, Pf(il.current));
          break;
        }
        case it: {
          var _ = (e.flags & ot) !== qe, A = ca(a, t.childLanes);
          if (_) {
            if (A)
              return Xb(e, t, a);
            t.flags |= ot;
          }
          var P = t.memoizedState;
          if (P !== null && (P.rendering = null, P.tail = null, P.lastEffect = null), $u(t, il.current), A)
            break;
          return null;
        }
        case Ie:
        case st:
          return t.lanes = Z, Vb(e, t, a);
      }
      return Mo(e, t, a);
    }
    function Zb(e, t, a) {
      if (t._debugNeedsRemount && e !== null)
        return kT(e, t, CS(t.type, t.key, t.pendingProps, t._debugOwner || null, t.mode, t.lanes));
      if (e !== null) {
        var i = e.memoizedProps, o = t.pendingProps;
        if (i !== o || Gh() || // Force a re-render if the implementation changed due to hot reload:
        t.type !== e.type)
          ul = !0;
        else {
          var s = W0(e, a);
          if (!s && // If this is the second pass of an error or suspense boundary, there
          // may not be work scheduled on `current`, so we check for this flag.
          (t.flags & ot) === qe)
            return ul = !1, _T(e, t, a);
          (e.flags & gs) !== qe ? ul = !0 : ul = !1;
        }
      } else if (ul = !1, Pr() && Zw(t)) {
        var f = t.index, p = eR();
        kx(t, p, f);
      }
      switch (t.lanes = Z, t.tag) {
        case ye:
          return sT(e, t, t.type, a);
        case be: {
          var v = t.elementType;
          return oT(e, t, v, a);
        }
        case B: {
          var g = t.type, x = t.pendingProps, N = t.elementType === g ? x : ol(g, x);
          return F0(e, t, g, N, a);
        }
        case K: {
          var _ = t.type, A = t.pendingProps, P = t.elementType === _ ? A : ol(_, A);
          return $b(e, t, _, P, a);
        }
        case ne:
          return aT(e, t, a);
        case V:
          return iT(e, t, a);
        case $:
          return lT(e, t);
        case ke:
          return Wb(e, t, a);
        case oe:
          return wT(e, t, a);
        case Ke: {
          var Q = t.type, ge = t.pendingProps, Xe = t.elementType === Q ? ge : ol(Q, ge);
          return Fb(e, t, Q, Xe, a);
        }
        case de:
          return tT(e, t, a);
        case Ae:
          return nT(e, t, a);
        case ct:
          return rT(e, t, a);
        case rt:
          return RT(e, t, a);
        case Dt:
          return TT(e, t, a);
        case at: {
          var Be = t.type, Ht = t.pendingProps, Mt = ol(Be, Ht);
          if (t.type !== t.elementType) {
            var L = Be.propTypes;
            L && nl(
              L,
              Mt,
              // Resolved for outer only
              "prop",
              zt(Be)
            );
          }
          return Mt = ol(Be.type, Mt), Hb(e, t, Be, Mt, a);
        }
        case Ye:
          return Pb(e, t, t.type, t.pendingProps, a);
        case Oe: {
          var G = t.type, j = t.pendingProps, le = t.elementType === G ? j : ol(G, j);
          return uT(e, t, G, le, a);
        }
        case it:
          return Xb(e, t, a);
        case Rt:
          break;
        case Ie:
          return Vb(e, t, a);
      }
      throw new Error("Unknown unit of work tag (" + t.tag + "). This error is likely caused by a bug in React. Please file an issue.");
    }
    function Wf(e) {
      e.flags |= xt;
    }
    function eC(e) {
      e.flags |= na, e.flags |= Nd;
    }
    var tC, Q0, nC, rC;
    tC = function(e, t, a, i) {
      for (var o = t.child; o !== null; ) {
        if (o.tag === V || o.tag === $)
          X1(e, o.stateNode);
        else if (o.tag !== oe) {
          if (o.child !== null) {
            o.child.return = o, o = o.child;
            continue;
          }
        }
        if (o === t)
          return;
        for (; o.sibling === null; ) {
          if (o.return === null || o.return === t)
            return;
          o = o.return;
        }
        o.sibling.return = o.return, o = o.sibling;
      }
    }, Q0 = function(e, t) {
    }, nC = function(e, t, a, i, o) {
      var s = e.memoizedProps;
      if (s !== i) {
        var f = t.stateNode, p = Vg(), v = J1(f, a, s, i, o, p);
        t.updateQueue = v, v && Wf(t);
      }
    }, rC = function(e, t, a, i) {
      a !== i && Wf(t);
    };
    function Yp(e, t) {
      if (!Pr())
        switch (e.tailMode) {
          case "hidden": {
            for (var a = e.tail, i = null; a !== null; )
              a.alternate !== null && (i = a), a = a.sibling;
            i === null ? e.tail = null : i.sibling = null;
            break;
          }
          case "collapsed": {
            for (var o = e.tail, s = null; o !== null; )
              o.alternate !== null && (s = o), o = o.sibling;
            s === null ? !t && e.tail !== null ? e.tail.sibling = null : e.tail = null : s.sibling = null;
            break;
          }
        }
    }
    function Br(e) {
      var t = e.alternate !== null && e.alternate.child === e.child, a = Z, i = qe;
      if (t) {
        if ((e.mode & ut) !== Fe) {
          for (var v = e.selfBaseDuration, g = e.child; g !== null; )
            a = gt(a, gt(g.lanes, g.childLanes)), i |= g.subtreeFlags & cr, i |= g.flags & cr, v += g.treeBaseDuration, g = g.sibling;
          e.treeBaseDuration = v;
        } else
          for (var x = e.child; x !== null; )
            a = gt(a, gt(x.lanes, x.childLanes)), i |= x.subtreeFlags & cr, i |= x.flags & cr, x.return = e, x = x.sibling;
        e.subtreeFlags |= i;
      } else {
        if ((e.mode & ut) !== Fe) {
          for (var o = e.actualDuration, s = e.selfBaseDuration, f = e.child; f !== null; )
            a = gt(a, gt(f.lanes, f.childLanes)), i |= f.subtreeFlags, i |= f.flags, o += f.actualDuration, s += f.treeBaseDuration, f = f.sibling;
          e.actualDuration = o, e.treeBaseDuration = s;
        } else
          for (var p = e.child; p !== null; )
            a = gt(a, gt(p.lanes, p.childLanes)), i |= p.subtreeFlags, i |= p.flags, p.return = e, p = p.sibling;
        e.subtreeFlags |= i;
      }
      return e.childLanes = a, t;
    }
    function DT(e, t, a) {
      if (pR() && (t.mode & Ve) !== Fe && (t.flags & ot) === qe)
        return jx(t), zf(), t.flags |= _n | Ca | ar, !1;
      var i = tm(t);
      if (a !== null && a.dehydrated !== null)
        if (e === null) {
          if (!i)
            throw new Error("A dehydrated suspense component was completed without a hydrated node. This is probably a bug in React.");
          if (fR(t), Br(t), (t.mode & ut) !== Fe) {
            var o = a !== null;
            if (o) {
              var s = t.child;
              s !== null && (t.treeBaseDuration -= s.treeBaseDuration);
            }
          }
          return !1;
        } else {
          if (zf(), (t.flags & ot) === qe && (t.memoizedState = null), t.flags |= xt, Br(t), (t.mode & ut) !== Fe) {
            var f = a !== null;
            if (f) {
              var p = t.child;
              p !== null && (t.treeBaseDuration -= p.treeBaseDuration);
            }
          }
          return !1;
        }
      else
        return zx(), !0;
    }
    function aC(e, t, a) {
      var i = t.pendingProps;
      switch (Sg(t), t.tag) {
        case ye:
        case be:
        case Ye:
        case B:
        case Ke:
        case de:
        case Ae:
        case ct:
        case Dt:
        case at:
          return Br(t), null;
        case K: {
          var o = t.type;
          return Bl(o) && qh(t), Br(t), null;
        }
        case ne: {
          var s = t.stateNode;
          if (Hf(t), hg(t), Wg(), s.pendingContext && (s.context = s.pendingContext, s.pendingContext = null), e === null || e.child === null) {
            var f = tm(t);
            if (f)
              Wf(t);
            else if (e !== null) {
              var p = e.memoizedState;
              // Check if this is a client root
              (!p.isDehydrated || // Check if we reverted to client rendering (e.g. due to an error)
              (t.flags & _n) !== qe) && (t.flags |= Ha, zx());
            }
          }
          return Q0(e, t), Br(t), null;
        }
        case V: {
          Bg(t);
          var v = Xx(), g = t.type;
          if (e !== null && t.stateNode != null)
            nC(e, t, g, i, v), e.ref !== t.ref && eC(t);
          else {
            if (!i) {
              if (t.stateNode === null)
                throw new Error("We must have new props for new mounts. This error is likely caused by a bug in React. Please file an issue.");
              return Br(t), null;
            }
            var x = Vg(), N = tm(t);
            if (N)
              sR(t, v, x) && Wf(t);
            else {
              var _ = q1(g, i, v, x, t);
              tC(_, t, !1, !1), t.stateNode = _, K1(_, g, i, v) && Wf(t);
            }
            t.ref !== null && eC(t);
          }
          return Br(t), null;
        }
        case $: {
          var A = i;
          if (e && t.stateNode != null) {
            var P = e.memoizedProps;
            rC(e, t, P, A);
          } else {
            if (typeof A != "string" && t.stateNode === null)
              throw new Error("We must have new props for new mounts. This error is likely caused by a bug in React. Please file an issue.");
            var Q = Xx(), ge = Vg(), Xe = tm(t);
            Xe ? cR(t) && Wf(t) : t.stateNode = Z1(A, Q, ge, t);
          }
          return Br(t), null;
        }
        case ke: {
          Vf(t);
          var Be = t.memoizedState;
          if (e === null || e.memoizedState !== null && e.memoizedState.dehydrated !== null) {
            var Ht = DT(e, t, Be);
            if (!Ht)
              return t.flags & ar ? t : null;
          }
          if ((t.flags & ot) !== qe)
            return t.lanes = a, (t.mode & ut) !== Fe && y0(t), t;
          var Mt = Be !== null, L = e !== null && e.memoizedState !== null;
          if (Mt !== L && Mt) {
            var G = t.child;
            if (G.flags |= Nl, (t.mode & Ve) !== Fe) {
              var j = e === null && (t.memoizedProps.unstable_avoidThisFallback !== !0 || !O);
              j || $g(il.current, Zx) ? Nk() : fS();
            }
          }
          var le = t.updateQueue;
          if (le !== null && (t.flags |= xt), Br(t), (t.mode & ut) !== Fe && Mt) {
            var we = t.child;
            we !== null && (t.treeBaseDuration -= we.treeBaseDuration);
          }
          return null;
        }
        case oe:
          return Hf(t), Q0(e, t), e === null && Ww(t.stateNode.containerInfo), Br(t), null;
        case rt:
          var xe = t.type._context;
          return Lg(xe, t), Br(t), null;
        case Oe: {
          var lt = t.type;
          return Bl(lt) && qh(t), Br(t), null;
        }
        case it: {
          Vf(t);
          var mt = t.memoizedState;
          if (mt === null)
            return Br(t), null;
          var an = (t.flags & ot) !== qe, It = mt.rendering;
          if (It === null)
            if (an)
              Yp(mt, !1);
            else {
              var Jn = Mk() && (e === null || (e.flags & ot) === qe);
              if (!Jn)
                for (var Yt = t.child; Yt !== null; ) {
                  var In = ym(Yt);
                  if (In !== null) {
                    an = !0, t.flags |= ot, Yp(mt, !1);
                    var ha = In.updateQueue;
                    return ha !== null && (t.updateQueue = ha, t.flags |= xt), t.subtreeFlags = qe, xR(t, a), $u(t, Ig(il.current, Mp)), t.child;
                  }
                  Yt = Yt.sibling;
                }
              mt.tail !== null && wn() > RC() && (t.flags |= ot, an = !0, Yp(mt, !1), t.lanes = eh);
            }
          else {
            if (!an) {
              var Qr = ym(It);
              if (Qr !== null) {
                t.flags |= ot, an = !0;
                var hi = Qr.updateQueue;
                if (hi !== null && (t.updateQueue = hi, t.flags |= xt), Yp(mt, !0), mt.tail === null && mt.tailMode === "hidden" && !It.alternate && !Pr())
                  return Br(t), null;
              } else
                // The time it took to render last row is greater than the remaining
                // time we have to render. So rendering one more row would likely
                // exceed it.
                wn() * 2 - mt.renderingStartTime > RC() && a !== _r && (t.flags |= ot, an = !0, Yp(mt, !1), t.lanes = eh);
            }
            if (mt.isBackwards)
              It.sibling = t.child, t.child = It;
            else {
              var Oa = mt.last;
              Oa !== null ? Oa.sibling = It : t.child = It, mt.last = It;
            }
          }
          if (mt.tail !== null) {
            var Ma = mt.tail;
            mt.rendering = Ma, mt.tail = Ma.sibling, mt.renderingStartTime = wn(), Ma.sibling = null;
            var ma = il.current;
            return an ? ma = Ig(ma, Mp) : ma = Pf(ma), $u(t, ma), Ma;
          }
          return Br(t), null;
        }
        case Rt:
          break;
        case Ie:
        case st: {
          cS(t);
          var Uo = t.memoizedState, ed = Uo !== null;
          if (e !== null) {
            var ov = e.memoizedState, Xl = ov !== null;
            Xl !== ed && // LegacyHidden doesn't do any hiding — it only pre-renders.
            !pe && (t.flags |= Nl);
          }
          return !ed || (t.mode & Ve) === Fe ? Br(t) : ca(ql, _r) && (Br(t), t.subtreeFlags & (pn | xt) && (t.flags |= Nl)), null;
        }
        case Nt:
          return null;
        case yt:
          return null;
      }
      throw new Error("Unknown unit of work tag (" + t.tag + "). This error is likely caused by a bug in React. Please file an issue.");
    }
    function NT(e, t, a) {
      switch (Sg(t), t.tag) {
        case K: {
          var i = t.type;
          Bl(i) && qh(t);
          var o = t.flags;
          return o & ar ? (t.flags = o & ~ar | ot, (t.mode & ut) !== Fe && y0(t), t) : null;
        }
        case ne: {
          t.stateNode, Hf(t), hg(t), Wg();
          var s = t.flags;
          return (s & ar) !== qe && (s & ot) === qe ? (t.flags = s & ~ar | ot, t) : null;
        }
        case V:
          return Bg(t), null;
        case ke: {
          Vf(t);
          var f = t.memoizedState;
          if (f !== null && f.dehydrated !== null) {
            if (t.alternate === null)
              throw new Error("Threw in newly mounted dehydrated component. This is likely a bug in React. Please file an issue.");
            zf();
          }
          var p = t.flags;
          return p & ar ? (t.flags = p & ~ar | ot, (t.mode & ut) !== Fe && y0(t), t) : null;
        }
        case it:
          return Vf(t), null;
        case oe:
          return Hf(t), null;
        case rt:
          var v = t.type._context;
          return Lg(v, t), null;
        case Ie:
        case st:
          return cS(t), null;
        case Nt:
          return null;
        default:
          return null;
      }
    }
    function iC(e, t, a) {
      switch (Sg(t), t.tag) {
        case K: {
          var i = t.type.childContextTypes;
          i != null && qh(t);
          break;
        }
        case ne: {
          t.stateNode, Hf(t), hg(t), Wg();
          break;
        }
        case V: {
          Bg(t);
          break;
        }
        case oe:
          Hf(t);
          break;
        case ke:
          Vf(t);
          break;
        case it:
          Vf(t);
          break;
        case rt:
          var o = t.type._context;
          Lg(o, t);
          break;
        case Ie:
        case st:
          cS(t);
          break;
      }
    }
    var lC = null;
    lC = /* @__PURE__ */ new Set();
    var Vm = !1, $r = !1, OT = typeof WeakSet == "function" ? WeakSet : Set, Ne = null, Qf = null, Gf = null;
    function MT(e) {
      oo(null, function() {
        throw e;
      }), _d();
    }
    var LT = function(e, t) {
      if (t.props = e.memoizedProps, t.state = e.memoizedState, e.mode & ut)
        try {
          Ql(), t.componentWillUnmount();
        } finally {
          Wl(e);
        }
      else
        t.componentWillUnmount();
    };
    function oC(e, t) {
      try {
        Wu(vr, e);
      } catch (a) {
        mn(e, t, a);
      }
    }
    function G0(e, t, a) {
      try {
        LT(e, a);
      } catch (i) {
        mn(e, t, i);
      }
    }
    function jT(e, t, a) {
      try {
        a.componentDidMount();
      } catch (i) {
        mn(e, t, i);
      }
    }
    function uC(e, t) {
      try {
        cC(e);
      } catch (a) {
        mn(e, t, a);
      }
    }
    function qf(e, t) {
      var a = e.ref;
      if (a !== null)
        if (typeof a == "function") {
          var i;
          try {
            if (vt && Ge && e.mode & ut)
              try {
                Ql(), i = a(null);
              } finally {
                Wl(e);
              }
            else
              i = a(null);
          } catch (o) {
            mn(e, t, o);
          }
          typeof i == "function" && y("Unexpected return value from a callback ref in %s. A callback ref should not return a function.", dt(e));
        } else
          a.current = null;
    }
    function Bm(e, t, a) {
      try {
        a();
      } catch (i) {
        mn(e, t, i);
      }
    }
    var sC = !1;
    function zT(e, t) {
      Q1(e.containerInfo), Ne = t, AT();
      var a = sC;
      return sC = !1, a;
    }
    function AT() {
      for (; Ne !== null; ) {
        var e = Ne, t = e.child;
        (e.subtreeFlags & iu) !== qe && t !== null ? (t.return = e, Ne = t) : UT();
      }
    }
    function UT() {
      for (; Ne !== null; ) {
        var e = Ne;
        Jt(e);
        try {
          FT(e);
        } catch (a) {
          mn(e, e.return, a);
        }
        kn();
        var t = e.sibling;
        if (t !== null) {
          t.return = e.return, Ne = t;
          return;
        }
        Ne = e.return;
      }
    }
    function FT(e) {
      var t = e.alternate, a = e.flags;
      if ((a & Ha) !== qe) {
        switch (Jt(e), e.tag) {
          case B:
          case Ke:
          case Ye:
            break;
          case K: {
            if (t !== null) {
              var i = t.memoizedProps, o = t.memoizedState, s = e.stateNode;
              e.type === e.elementType && !Zs && (s.props !== e.memoizedProps && y("Expected %s props to match memoized props before getSnapshotBeforeUpdate. This might either be because of a bug in React, or because a component reassigns its own `this.props`. Please file an issue.", dt(e) || "instance"), s.state !== e.memoizedState && y("Expected %s state to match memoized state before getSnapshotBeforeUpdate. This might either be because of a bug in React, or because a component reassigns its own `this.state`. Please file an issue.", dt(e) || "instance"));
              var f = s.getSnapshotBeforeUpdate(e.elementType === e.type ? i : ol(e.type, i), o);
              {
                var p = lC;
                f === void 0 && !p.has(e.type) && (p.add(e.type), y("%s.getSnapshotBeforeUpdate(): A snapshot value (or null) must be returned. You have returned undefined.", dt(e)));
              }
              s.__reactInternalSnapshotBeforeUpdate = f;
            }
            break;
          }
          case ne: {
            {
              var v = e.stateNode;
              gw(v.containerInfo);
            }
            break;
          }
          case V:
          case $:
          case oe:
          case Oe:
            break;
          default:
            throw new Error("This unit of work tag should not have side-effects. This error is likely caused by a bug in React. Please file an issue.");
        }
        kn();
      }
    }
    function sl(e, t, a) {
      var i = t.updateQueue, o = i !== null ? i.lastEffect : null;
      if (o !== null) {
        var s = o.next, f = s;
        do {
          if ((f.tag & e) === e) {
            var p = f.destroy;
            f.destroy = void 0, p !== void 0 && ((e & Vr) !== Za ? Kv(t) : (e & vr) !== Za && di(t), (e & $l) !== Za && av(!0), Bm(t, a, p), (e & $l) !== Za && av(!1), (e & Vr) !== Za ? jc() : (e & vr) !== Za && su());
          }
          f = f.next;
        } while (f !== s);
      }
    }
    function Wu(e, t) {
      var a = t.updateQueue, i = a !== null ? a.lastEffect : null;
      if (i !== null) {
        var o = i.next, s = o;
        do {
          if ((s.tag & e) === e) {
            (e & Vr) !== Za ? Ll(t) : (e & vr) !== Za && Jv(t);
            var f = s.create;
            (e & $l) !== Za && av(!0), s.destroy = f(), (e & $l) !== Za && av(!1), (e & Vr) !== Za ? Lc() : (e & vr) !== Za && Ss();
            {
              var p = s.destroy;
              if (p !== void 0 && typeof p != "function") {
                var v = void 0;
                (s.tag & vr) !== qe ? v = "useLayoutEffect" : (s.tag & $l) !== qe ? v = "useInsertionEffect" : v = "useEffect";
                var g = void 0;
                p === null ? g = " You returned null. If your effect does not require clean up, return undefined (or nothing)." : typeof p.then == "function" ? g = `

It looks like you wrote ` + v + `(async () => ...) or returned a Promise. Instead, write the async function inside your effect and call it immediately:

` + v + `(() => {
  async function fetchData() {
    // You can await here
    const response = await MyAPI.getData(someId);
    // ...
  }
  fetchData();
}, [someId]); // Or [] if effect doesn't need props or state

Learn more about data fetching with Hooks: https://reactjs.org/link/hooks-data-fetching` : g = " You returned: " + p, y("%s must not return anything besides a function, which is used for clean-up.%s", v, g);
              }
            }
          }
          s = s.next;
        } while (s !== o);
      }
    }
    function HT(e, t) {
      if ((t.flags & xt) !== qe)
        switch (t.tag) {
          case ct: {
            var a = t.stateNode.passiveEffectDuration, i = t.memoizedProps, o = i.id, s = i.onPostCommit, f = Rb(), p = t.alternate === null ? "mount" : "update";
            wb() && (p = "nested-update"), typeof s == "function" && s(o, p, a, f);
            var v = t.return;
            e:
              for (; v !== null; ) {
                switch (v.tag) {
                  case ne:
                    var g = v.stateNode;
                    g.passiveEffectDuration += a;
                    break e;
                  case ct:
                    var x = v.stateNode;
                    x.passiveEffectDuration += a;
                    break e;
                }
                v = v.return;
              }
            break;
          }
        }
    }
    function PT(e, t, a, i) {
      if ((a.flags & Tr) !== qe)
        switch (a.tag) {
          case B:
          case Ke:
          case Ye: {
            if (!$r)
              if (a.mode & ut)
                try {
                  Ql(), Wu(vr | pr, a);
                } finally {
                  Wl(a);
                }
              else
                Wu(vr | pr, a);
            break;
          }
          case K: {
            var o = a.stateNode;
            if (a.flags & xt && !$r)
              if (t === null)
                if (a.type === a.elementType && !Zs && (o.props !== a.memoizedProps && y("Expected %s props to match memoized props before componentDidMount. This might either be because of a bug in React, or because a component reassigns its own `this.props`. Please file an issue.", dt(a) || "instance"), o.state !== a.memoizedState && y("Expected %s state to match memoized state before componentDidMount. This might either be because of a bug in React, or because a component reassigns its own `this.state`. Please file an issue.", dt(a) || "instance")), a.mode & ut)
                  try {
                    Ql(), o.componentDidMount();
                  } finally {
                    Wl(a);
                  }
                else
                  o.componentDidMount();
              else {
                var s = a.elementType === a.type ? t.memoizedProps : ol(a.type, t.memoizedProps), f = t.memoizedState;
                if (a.type === a.elementType && !Zs && (o.props !== a.memoizedProps && y("Expected %s props to match memoized props before componentDidUpdate. This might either be because of a bug in React, or because a component reassigns its own `this.props`. Please file an issue.", dt(a) || "instance"), o.state !== a.memoizedState && y("Expected %s state to match memoized state before componentDidUpdate. This might either be because of a bug in React, or because a component reassigns its own `this.state`. Please file an issue.", dt(a) || "instance")), a.mode & ut)
                  try {
                    Ql(), o.componentDidUpdate(s, f, o.__reactInternalSnapshotBeforeUpdate);
                  } finally {
                    Wl(a);
                  }
                else
                  o.componentDidUpdate(s, f, o.__reactInternalSnapshotBeforeUpdate);
              }
            var p = a.updateQueue;
            p !== null && (a.type === a.elementType && !Zs && (o.props !== a.memoizedProps && y("Expected %s props to match memoized props before processing the update queue. This might either be because of a bug in React, or because a component reassigns its own `this.props`. Please file an issue.", dt(a) || "instance"), o.state !== a.memoizedState && y("Expected %s state to match memoized state before processing the update queue. This might either be because of a bug in React, or because a component reassigns its own `this.state`. Please file an issue.", dt(a) || "instance")), qx(a, p, o));
            break;
          }
          case ne: {
            var v = a.updateQueue;
            if (v !== null) {
              var g = null;
              if (a.child !== null)
                switch (a.child.tag) {
                  case V:
                    g = a.child.stateNode;
                    break;
                  case K:
                    g = a.child.stateNode;
                    break;
                }
              qx(a, v, g);
            }
            break;
          }
          case V: {
            var x = a.stateNode;
            if (t === null && a.flags & xt) {
              var N = a.type, _ = a.memoizedProps;
              aw(x, N, _);
            }
            break;
          }
          case $:
            break;
          case oe:
            break;
          case ct: {
            {
              var A = a.memoizedProps, P = A.onCommit, Q = A.onRender, ge = a.stateNode.effectDuration, Xe = Rb(), Be = t === null ? "mount" : "update";
              wb() && (Be = "nested-update"), typeof Q == "function" && Q(a.memoizedProps.id, Be, a.actualDuration, a.treeBaseDuration, a.actualStartTime, Xe);
              {
                typeof P == "function" && P(a.memoizedProps.id, Be, ge, Xe), Uk(a);
                var Ht = a.return;
                e:
                  for (; Ht !== null; ) {
                    switch (Ht.tag) {
                      case ne:
                        var Mt = Ht.stateNode;
                        Mt.effectDuration += ge;
                        break e;
                      case ct:
                        var L = Ht.stateNode;
                        L.effectDuration += ge;
                        break e;
                    }
                    Ht = Ht.return;
                  }
              }
            }
            break;
          }
          case ke: {
            GT(e, a);
            break;
          }
          case it:
          case Oe:
          case Rt:
          case Ie:
          case st:
          case yt:
            break;
          default:
            throw new Error("This unit of work tag should not have side-effects. This error is likely caused by a bug in React. Please file an issue.");
        }
      $r || a.flags & na && cC(a);
    }
    function VT(e) {
      switch (e.tag) {
        case B:
        case Ke:
        case Ye: {
          if (e.mode & ut)
            try {
              Ql(), oC(e, e.return);
            } finally {
              Wl(e);
            }
          else
            oC(e, e.return);
          break;
        }
        case K: {
          var t = e.stateNode;
          typeof t.componentDidMount == "function" && jT(e, e.return, t), uC(e, e.return);
          break;
        }
        case V: {
          uC(e, e.return);
          break;
        }
      }
    }
    function BT(e, t) {
      for (var a = null, i = e; ; ) {
        if (i.tag === V) {
          if (a === null) {
            a = i;
            try {
              var o = i.stateNode;
              t ? vw(o) : mw(i.stateNode, i.memoizedProps);
            } catch (f) {
              mn(e, e.return, f);
            }
          }
        } else if (i.tag === $) {
          if (a === null)
            try {
              var s = i.stateNode;
              t ? hw(s) : yw(s, i.memoizedProps);
            } catch (f) {
              mn(e, e.return, f);
            }
        } else if (!((i.tag === Ie || i.tag === st) && i.memoizedState !== null && i !== e)) {
          if (i.child !== null) {
            i.child.return = i, i = i.child;
            continue;
          }
        }
        if (i === e)
          return;
        for (; i.sibling === null; ) {
          if (i.return === null || i.return === e)
            return;
          a === i && (a = null), i = i.return;
        }
        a === i && (a = null), i.sibling.return = i.return, i = i.sibling;
      }
    }
    function cC(e) {
      var t = e.ref;
      if (t !== null) {
        var a = e.stateNode, i;
        switch (e.tag) {
          case V:
            i = a;
            break;
          default:
            i = a;
        }
        if (typeof t == "function") {
          var o;
          if (e.mode & ut)
            try {
              Ql(), o = t(i);
            } finally {
              Wl(e);
            }
          else
            o = t(i);
          typeof o == "function" && y("Unexpected return value from a callback ref in %s. A callback ref should not return a function.", dt(e));
        } else
          t.hasOwnProperty("current") || y("Unexpected ref object provided for %s. Use either a ref-setter function or React.createRef().", dt(e)), t.current = i;
      }
    }
    function $T(e) {
      var t = e.alternate;
      t !== null && (t.return = null), e.return = null;
    }
    function fC(e) {
      var t = e.alternate;
      t !== null && (e.alternate = null, fC(t));
      {
        if (e.child = null, e.deletions = null, e.sibling = null, e.tag === V) {
          var a = e.stateNode;
          a !== null && qw(a);
        }
        e.stateNode = null, e._debugOwner = null, e.return = null, e.dependencies = null, e.memoizedProps = null, e.memoizedState = null, e.pendingProps = null, e.stateNode = null, e.updateQueue = null;
      }
    }
    function IT(e) {
      for (var t = e.return; t !== null; ) {
        if (dC(t))
          return t;
        t = t.return;
      }
      throw new Error("Expected to find a host parent. This error is likely caused by a bug in React. Please file an issue.");
    }
    function dC(e) {
      return e.tag === V || e.tag === ne || e.tag === oe;
    }
    function pC(e) {
      var t = e;
      e:
        for (; ; ) {
          for (; t.sibling === null; ) {
            if (t.return === null || dC(t.return))
              return null;
            t = t.return;
          }
          for (t.sibling.return = t.return, t = t.sibling; t.tag !== V && t.tag !== $ && t.tag !== $e; ) {
            if (t.flags & pn || t.child === null || t.tag === oe)
              continue e;
            t.child.return = t, t = t.child;
          }
          if (!(t.flags & pn))
            return t.stateNode;
        }
    }
    function YT(e) {
      var t = IT(e);
      switch (t.tag) {
        case V: {
          var a = t.stateNode;
          t.flags & Zt && (hx(a), t.flags &= ~Zt);
          var i = pC(e);
          X0(e, i, a);
          break;
        }
        case ne:
        case oe: {
          var o = t.stateNode.containerInfo, s = pC(e);
          q0(e, s, o);
          break;
        }
        default:
          throw new Error("Invalid host parent fiber. This error is likely caused by a bug in React. Please file an issue.");
      }
    }
    function q0(e, t, a) {
      var i = e.tag, o = i === V || i === $;
      if (o) {
        var s = e.stateNode;
        t ? cw(a, s, t) : uw(a, s);
      } else if (i !== oe) {
        var f = e.child;
        if (f !== null) {
          q0(f, t, a);
          for (var p = f.sibling; p !== null; )
            q0(p, t, a), p = p.sibling;
        }
      }
    }
    function X0(e, t, a) {
      var i = e.tag, o = i === V || i === $;
      if (o) {
        var s = e.stateNode;
        t ? sw(a, s, t) : ow(a, s);
      } else if (i !== oe) {
        var f = e.child;
        if (f !== null) {
          X0(f, t, a);
          for (var p = f.sibling; p !== null; )
            X0(p, t, a), p = p.sibling;
        }
      }
    }
    var Ir = null, cl = !1;
    function WT(e, t, a) {
      {
        var i = t;
        e:
          for (; i !== null; ) {
            switch (i.tag) {
              case V: {
                Ir = i.stateNode, cl = !1;
                break e;
              }
              case ne: {
                Ir = i.stateNode.containerInfo, cl = !0;
                break e;
              }
              case oe: {
                Ir = i.stateNode.containerInfo, cl = !0;
                break e;
              }
            }
            i = i.return;
          }
        if (Ir === null)
          throw new Error("Expected to find a host parent. This error is likely caused by a bug in React. Please file an issue.");
        vC(e, t, a), Ir = null, cl = !1;
      }
      $T(a);
    }
    function Qu(e, t, a) {
      for (var i = a.child; i !== null; )
        vC(e, t, i), i = i.sibling;
    }
    function vC(e, t, a) {
      switch (co(a), a.tag) {
        case V:
          $r || qf(a, t);
        case $: {
          {
            var i = Ir, o = cl;
            Ir = null, Qu(e, t, a), Ir = i, cl = o, Ir !== null && (cl ? dw(Ir, a.stateNode) : fw(Ir, a.stateNode));
          }
          return;
        }
        case $e: {
          Ir !== null && (cl ? pw(Ir, a.stateNode) : og(Ir, a.stateNode));
          return;
        }
        case oe: {
          {
            var s = Ir, f = cl;
            Ir = a.stateNode.containerInfo, cl = !0, Qu(e, t, a), Ir = s, cl = f;
          }
          return;
        }
        case B:
        case Ke:
        case at:
        case Ye: {
          if (!$r) {
            var p = a.updateQueue;
            if (p !== null) {
              var v = p.lastEffect;
              if (v !== null) {
                var g = v.next, x = g;
                do {
                  var N = x, _ = N.destroy, A = N.tag;
                  _ !== void 0 && ((A & $l) !== Za ? Bm(a, t, _) : (A & vr) !== Za && (di(a), a.mode & ut ? (Ql(), Bm(a, t, _), Wl(a)) : Bm(a, t, _), su())), x = x.next;
                } while (x !== g);
              }
            }
          }
          Qu(e, t, a);
          return;
        }
        case K: {
          if (!$r) {
            qf(a, t);
            var P = a.stateNode;
            typeof P.componentWillUnmount == "function" && G0(a, t, P);
          }
          Qu(e, t, a);
          return;
        }
        case Rt: {
          Qu(e, t, a);
          return;
        }
        case Ie: {
          if (
            // TODO: Remove this dead flag
            a.mode & Ve
          ) {
            var Q = $r;
            $r = Q || a.memoizedState !== null, Qu(e, t, a), $r = Q;
          } else
            Qu(e, t, a);
          break;
        }
        default: {
          Qu(e, t, a);
          return;
        }
      }
    }
    function QT(e) {
      e.memoizedState;
    }
    function GT(e, t) {
      var a = t.memoizedState;
      if (a === null) {
        var i = t.alternate;
        if (i !== null) {
          var o = i.memoizedState;
          if (o !== null) {
            var s = o.dehydrated;
            s !== null && Mw(s);
          }
        }
      }
    }
    function hC(e) {
      var t = e.updateQueue;
      if (t !== null) {
        e.updateQueue = null;
        var a = e.stateNode;
        a === null && (a = e.stateNode = new OT()), t.forEach(function(i) {
          var o = Ik.bind(null, e, i);
          if (!a.has(i)) {
            if (a.add(i), Ra)
              if (Qf !== null && Gf !== null)
                rv(Gf, Qf);
              else
                throw Error("Expected finished root and lanes to be set. This is a bug in React.");
            i.then(o, o);
          }
        });
      }
    }
    function qT(e, t, a) {
      Qf = a, Gf = e, Jt(t), mC(t, e), Jt(t), Qf = null, Gf = null;
    }
    function fl(e, t, a) {
      var i = t.deletions;
      if (i !== null)
        for (var o = 0; o < i.length; o++) {
          var s = i[o];
          try {
            WT(e, t, s);
          } catch (v) {
            mn(s, t, v);
          }
        }
      var f = fc();
      if (t.subtreeFlags & ia)
        for (var p = t.child; p !== null; )
          Jt(p), mC(p, e), p = p.sibling;
      Jt(f);
    }
    function mC(e, t, a) {
      var i = e.alternate, o = e.flags;
      switch (e.tag) {
        case B:
        case Ke:
        case at:
        case Ye: {
          if (fl(t, e), Gl(e), o & xt) {
            try {
              sl($l | pr, e, e.return), Wu($l | pr, e);
            } catch (lt) {
              mn(e, e.return, lt);
            }
            if (e.mode & ut) {
              try {
                Ql(), sl(vr | pr, e, e.return);
              } catch (lt) {
                mn(e, e.return, lt);
              }
              Wl(e);
            } else
              try {
                sl(vr | pr, e, e.return);
              } catch (lt) {
                mn(e, e.return, lt);
              }
          }
          return;
        }
        case K: {
          fl(t, e), Gl(e), o & na && i !== null && qf(i, i.return);
          return;
        }
        case V: {
          fl(t, e), Gl(e), o & na && i !== null && qf(i, i.return);
          {
            if (e.flags & Zt) {
              var s = e.stateNode;
              try {
                hx(s);
              } catch (lt) {
                mn(e, e.return, lt);
              }
            }
            if (o & xt) {
              var f = e.stateNode;
              if (f != null) {
                var p = e.memoizedProps, v = i !== null ? i.memoizedProps : p, g = e.type, x = e.updateQueue;
                if (e.updateQueue = null, x !== null)
                  try {
                    iw(f, x, g, v, p, e);
                  } catch (lt) {
                    mn(e, e.return, lt);
                  }
              }
            }
          }
          return;
        }
        case $: {
          if (fl(t, e), Gl(e), o & xt) {
            if (e.stateNode === null)
              throw new Error("This should have a text node initialized. This error is likely caused by a bug in React. Please file an issue.");
            var N = e.stateNode, _ = e.memoizedProps, A = i !== null ? i.memoizedProps : _;
            try {
              lw(N, A, _);
            } catch (lt) {
              mn(e, e.return, lt);
            }
          }
          return;
        }
        case ne: {
          if (fl(t, e), Gl(e), o & xt && i !== null) {
            var P = i.memoizedState;
            if (P.isDehydrated)
              try {
                Ow(t.containerInfo);
              } catch (lt) {
                mn(e, e.return, lt);
              }
          }
          return;
        }
        case oe: {
          fl(t, e), Gl(e);
          return;
        }
        case ke: {
          fl(t, e), Gl(e);
          var Q = e.child;
          if (Q.flags & Nl) {
            var ge = Q.stateNode, Xe = Q.memoizedState, Be = Xe !== null;
            if (ge.isHidden = Be, Be) {
              var Ht = Q.alternate !== null && Q.alternate.memoizedState !== null;
              Ht || Dk();
            }
          }
          if (o & xt) {
            try {
              QT(e);
            } catch (lt) {
              mn(e, e.return, lt);
            }
            hC(e);
          }
          return;
        }
        case Ie: {
          var Mt = i !== null && i.memoizedState !== null;
          if (
            // TODO: Remove this dead flag
            e.mode & Ve
          ) {
            var L = $r;
            $r = L || Mt, fl(t, e), $r = L;
          } else
            fl(t, e);
          if (Gl(e), o & Nl) {
            var G = e.stateNode, j = e.memoizedState, le = j !== null, we = e;
            if (G.isHidden = le, le && !Mt && (we.mode & Ve) !== Fe) {
              Ne = we;
              for (var xe = we.child; xe !== null; )
                Ne = xe, KT(xe), xe = xe.sibling;
            }
            BT(we, le);
          }
          return;
        }
        case it: {
          fl(t, e), Gl(e), o & xt && hC(e);
          return;
        }
        case Rt:
          return;
        default: {
          fl(t, e), Gl(e);
          return;
        }
      }
    }
    function Gl(e) {
      var t = e.flags;
      if (t & pn) {
        try {
          YT(e);
        } catch (a) {
          mn(e, e.return, a);
        }
        e.flags &= ~pn;
      }
      t & Pa && (e.flags &= ~Pa);
    }
    function XT(e, t, a) {
      Qf = a, Gf = t, Ne = e, yC(e, t, a), Qf = null, Gf = null;
    }
    function yC(e, t, a) {
      for (var i = (e.mode & Ve) !== Fe; Ne !== null; ) {
        var o = Ne, s = o.child;
        if (o.tag === Ie && i) {
          var f = o.memoizedState !== null, p = f || Vm;
          if (p) {
            K0(e, t, a);
            continue;
          } else {
            var v = o.alternate, g = v !== null && v.memoizedState !== null, x = g || $r, N = Vm, _ = $r;
            Vm = p, $r = x, $r && !_ && (Ne = o, JT(o));
            for (var A = s; A !== null; )
              Ne = A, yC(
                A,
                // New root; bubble back up to here and stop.
                t,
                a
              ), A = A.sibling;
            Ne = o, Vm = N, $r = _, K0(e, t, a);
            continue;
          }
        }
        (o.subtreeFlags & Tr) !== qe && s !== null ? (s.return = o, Ne = s) : K0(e, t, a);
      }
    }
    function K0(e, t, a) {
      for (; Ne !== null; ) {
        var i = Ne;
        if ((i.flags & Tr) !== qe) {
          var o = i.alternate;
          Jt(i);
          try {
            PT(t, o, i, a);
          } catch (f) {
            mn(i, i.return, f);
          }
          kn();
        }
        if (i === e) {
          Ne = null;
          return;
        }
        var s = i.sibling;
        if (s !== null) {
          s.return = i.return, Ne = s;
          return;
        }
        Ne = i.return;
      }
    }
    function KT(e) {
      for (; Ne !== null; ) {
        var t = Ne, a = t.child;
        switch (t.tag) {
          case B:
          case Ke:
          case at:
          case Ye: {
            if (t.mode & ut)
              try {
                Ql(), sl(vr, t, t.return);
              } finally {
                Wl(t);
              }
            else
              sl(vr, t, t.return);
            break;
          }
          case K: {
            qf(t, t.return);
            var i = t.stateNode;
            typeof i.componentWillUnmount == "function" && G0(t, t.return, i);
            break;
          }
          case V: {
            qf(t, t.return);
            break;
          }
          case Ie: {
            var o = t.memoizedState !== null;
            if (o) {
              gC(e);
              continue;
            }
            break;
          }
        }
        a !== null ? (a.return = t, Ne = a) : gC(e);
      }
    }
    function gC(e) {
      for (; Ne !== null; ) {
        var t = Ne;
        if (t === e) {
          Ne = null;
          return;
        }
        var a = t.sibling;
        if (a !== null) {
          a.return = t.return, Ne = a;
          return;
        }
        Ne = t.return;
      }
    }
    function JT(e) {
      for (; Ne !== null; ) {
        var t = Ne, a = t.child;
        if (t.tag === Ie) {
          var i = t.memoizedState !== null;
          if (i) {
            SC(e);
            continue;
          }
        }
        a !== null ? (a.return = t, Ne = a) : SC(e);
      }
    }
    function SC(e) {
      for (; Ne !== null; ) {
        var t = Ne;
        Jt(t);
        try {
          VT(t);
        } catch (i) {
          mn(t, t.return, i);
        }
        if (kn(), t === e) {
          Ne = null;
          return;
        }
        var a = t.sibling;
        if (a !== null) {
          a.return = t.return, Ne = a;
          return;
        }
        Ne = t.return;
      }
    }
    function ZT(e, t, a, i) {
      Ne = t, ek(t, e, a, i);
    }
    function ek(e, t, a, i) {
      for (; Ne !== null; ) {
        var o = Ne, s = o.child;
        (o.subtreeFlags & Va) !== qe && s !== null ? (s.return = o, Ne = s) : tk(e, t, a, i);
      }
    }
    function tk(e, t, a, i) {
      for (; Ne !== null; ) {
        var o = Ne;
        if ((o.flags & yn) !== qe) {
          Jt(o);
          try {
            nk(t, o, a, i);
          } catch (f) {
            mn(o, o.return, f);
          }
          kn();
        }
        if (o === e) {
          Ne = null;
          return;
        }
        var s = o.sibling;
        if (s !== null) {
          s.return = o.return, Ne = s;
          return;
        }
        Ne = o.return;
      }
    }
    function nk(e, t, a, i) {
      switch (t.tag) {
        case B:
        case Ke:
        case Ye: {
          if (t.mode & ut) {
            m0();
            try {
              Wu(Vr | pr, t);
            } finally {
              h0(t);
            }
          } else
            Wu(Vr | pr, t);
          break;
        }
      }
    }
    function rk(e) {
      Ne = e, ak();
    }
    function ak() {
      for (; Ne !== null; ) {
        var e = Ne, t = e.child;
        if ((Ne.flags & Gt) !== qe) {
          var a = e.deletions;
          if (a !== null) {
            for (var i = 0; i < a.length; i++) {
              var o = a[i];
              Ne = o, ok(o, e);
            }
            {
              var s = e.alternate;
              if (s !== null) {
                var f = s.child;
                if (f !== null) {
                  s.child = null;
                  do {
                    var p = f.sibling;
                    f.sibling = null, f = p;
                  } while (f !== null);
                }
              }
            }
            Ne = e;
          }
        }
        (e.subtreeFlags & Va) !== qe && t !== null ? (t.return = e, Ne = t) : ik();
      }
    }
    function ik() {
      for (; Ne !== null; ) {
        var e = Ne;
        (e.flags & yn) !== qe && (Jt(e), lk(e), kn());
        var t = e.sibling;
        if (t !== null) {
          t.return = e.return, Ne = t;
          return;
        }
        Ne = e.return;
      }
    }
    function lk(e) {
      switch (e.tag) {
        case B:
        case Ke:
        case Ye: {
          e.mode & ut ? (m0(), sl(Vr | pr, e, e.return), h0(e)) : sl(Vr | pr, e, e.return);
          break;
        }
      }
    }
    function ok(e, t) {
      for (; Ne !== null; ) {
        var a = Ne;
        Jt(a), sk(a, t), kn();
        var i = a.child;
        i !== null ? (i.return = a, Ne = i) : uk(e);
      }
    }
    function uk(e) {
      for (; Ne !== null; ) {
        var t = Ne, a = t.sibling, i = t.return;
        if (fC(t), t === e) {
          Ne = null;
          return;
        }
        if (a !== null) {
          a.return = i, Ne = a;
          return;
        }
        Ne = i;
      }
    }
    function sk(e, t) {
      switch (e.tag) {
        case B:
        case Ke:
        case Ye: {
          e.mode & ut ? (m0(), sl(Vr, e, t), h0(e)) : sl(Vr, e, t);
          break;
        }
      }
    }
    function ck(e) {
      switch (e.tag) {
        case B:
        case Ke:
        case Ye: {
          try {
            Wu(vr | pr, e);
          } catch (a) {
            mn(e, e.return, a);
          }
          break;
        }
        case K: {
          var t = e.stateNode;
          try {
            t.componentDidMount();
          } catch (a) {
            mn(e, e.return, a);
          }
          break;
        }
      }
    }
    function fk(e) {
      switch (e.tag) {
        case B:
        case Ke:
        case Ye: {
          try {
            Wu(Vr | pr, e);
          } catch (t) {
            mn(e, e.return, t);
          }
          break;
        }
      }
    }
    function dk(e) {
      switch (e.tag) {
        case B:
        case Ke:
        case Ye: {
          try {
            sl(vr | pr, e, e.return);
          } catch (a) {
            mn(e, e.return, a);
          }
          break;
        }
        case K: {
          var t = e.stateNode;
          typeof t.componentWillUnmount == "function" && G0(e, e.return, t);
          break;
        }
      }
    }
    function pk(e) {
      switch (e.tag) {
        case B:
        case Ke:
        case Ye:
          try {
            sl(Vr | pr, e, e.return);
          } catch (t) {
            mn(e, e.return, t);
          }
      }
    }
    if (typeof Symbol == "function" && Symbol.for) {
      var Wp = Symbol.for;
      Wp("selector.component"), Wp("selector.has_pseudo_class"), Wp("selector.role"), Wp("selector.test_id"), Wp("selector.text");
    }
    var vk = [];
    function hk() {
      vk.forEach(function(e) {
        return e();
      });
    }
    var mk = b.ReactCurrentActQueue;
    function yk(e) {
      {
        var t = (
          // $FlowExpectedError – Flow doesn't know about IS_REACT_ACT_ENVIRONMENT globalThis
          typeof IS_REACT_ACT_ENVIRONMENT < "u" ? IS_REACT_ACT_ENVIRONMENT : void 0
        ), a = typeof jest < "u";
        return a && t !== !1;
      }
    }
    function xC() {
      {
        var e = (
          // $FlowExpectedError – Flow doesn't know about IS_REACT_ACT_ENVIRONMENT globalThis
          typeof IS_REACT_ACT_ENVIRONMENT < "u" ? IS_REACT_ACT_ENVIRONMENT : void 0
        );
        return !e && mk.current !== null && y("The current testing environment is not configured to support act(...)"), e;
      }
    }
    var gk = Math.ceil, J0 = b.ReactCurrentDispatcher, Z0 = b.ReactCurrentOwner, Yr = b.ReactCurrentBatchConfig, dl = b.ReactCurrentActQueue, yr = (
      /*             */
      0
    ), bC = (
      /*               */
      1
    ), Wr = (
      /*                */
      2
    ), zi = (
      /*                */
      4
    ), Lo = 0, Qp = 1, ec = 2, $m = 3, Gp = 4, CC = 5, eS = 6, Ft = yr, Da = null, Un = null, gr = Z, ql = Z, tS = Uu(Z), Sr = Lo, qp = null, Im = Z, Xp = Z, Ym = Z, Kp = null, ei = null, nS = 0, EC = 500, wC = 1 / 0, Sk = 500, jo = null;
    function Jp() {
      wC = wn() + Sk;
    }
    function RC() {
      return wC;
    }
    var Wm = !1, rS = null, Xf = null, tc = !1, Gu = null, Zp = Z, aS = [], iS = null, xk = 50, ev = 0, lS = null, oS = !1, Qm = !1, bk = 50, Kf = 0, Gm = null, tv = fn, qm = Z, TC = !1;
    function Xm() {
      return Da;
    }
    function Na() {
      return (Ft & (Wr | zi)) !== yr ? wn() : (tv !== fn || (tv = wn()), tv);
    }
    function qu(e) {
      var t = e.mode;
      if ((t & Ve) === Fe)
        return Qe;
      if ((Ft & Wr) !== yr && gr !== Z)
        return gu(gr);
      var a = mR() !== hR;
      if (a) {
        if (Yr.transition !== null) {
          var i = Yr.transition;
          i._updatedFibers || (i._updatedFibers = /* @__PURE__ */ new Set()), i._updatedFibers.add(e);
        }
        return qm === $n && (qm = uh()), qm;
      }
      var o = Wa();
      if (o !== $n)
        return o;
      var s = ew();
      return s;
    }
    function Ck(e) {
      var t = e.mode;
      return (t & Ve) === Fe ? Qe : sa();
    }
    function xr(e, t, a, i) {
      Wk(), TC && y("useInsertionEffect must not schedule updates."), oS && (Qm = !0), So(e, a, i), (Ft & Wr) !== Z && e === Da ? qk(t) : (Ra && rf(e, t, a), Xk(t), e === Da && ((Ft & Wr) === yr && (Xp = gt(Xp, a)), Sr === Gp && Xu(e, gr)), ti(e, i), a === Qe && Ft === yr && (t.mode & Ve) === Fe && // Treat `act` as if it's inside `batchedUpdates`, even in legacy mode.
      !dl.isBatchingLegacy && (Jp(), Tx()));
    }
    function Ek(e, t, a) {
      var i = e.current;
      i.lanes = t, So(e, t, a), ti(e, a);
    }
    function wk(e) {
      return (
        // TODO: Remove outdated deferRenderPhaseUpdateToNextBatch experiment. We
        // decided not to enable it.
        (Ft & Wr) !== yr
      );
    }
    function ti(e, t) {
      var a = e.callbackNode;
      rh(e, t);
      var i = yo(e, e === Da ? gr : Z);
      if (i === Z) {
        a !== null && BC(a), e.callbackNode = null, e.callbackPriority = $n;
        return;
      }
      var o = jn(i), s = e.callbackPriority;
      if (s === o && // Special case related to `act`. If the currently scheduled task is a
      // Scheduler task, rather than an `act` task, cancel it and re-scheduled
      // on the `act` queue.
      !(dl.current !== null && a !== vS)) {
        a == null && s !== Qe && y("Expected scheduled callback to exist. This error is likely caused by a bug in React. Please file an issue.");
        return;
      }
      a != null && BC(a);
      var f;
      if (o === Qe)
        e.tag === Fu ? (dl.isBatchingLegacy !== null && (dl.didScheduleLegacyUpdate = !0), Jw(DC.bind(null, e))) : Rx(DC.bind(null, e)), dl.current !== null ? dl.current.push(Hu) : nw(function() {
          (Ft & (Wr | zi)) === yr && Hu();
        }), f = null;
      else {
        var p;
        switch (dr(i)) {
          case zn:
            p = Nc;
            break;
          case Ji:
            p = so;
            break;
          case Ti:
            p = Ri;
            break;
          case Su:
            p = Oc;
            break;
          default:
            p = Ri;
            break;
        }
        f = hS(p, kC.bind(null, e));
      }
      e.callbackPriority = o, e.callbackNode = f;
    }
    function kC(e, t) {
      if (BR(), tv = fn, qm = Z, (Ft & (Wr | zi)) !== yr)
        throw new Error("Should not already be working.");
      var a = e.callbackNode, i = Ao();
      if (i && e.callbackNode !== a)
        return null;
      var o = yo(e, e === Da ? gr : Z);
      if (o === Z)
        return null;
      var s = !ks(e, o) && !oh(e, o) && !t, f = s ? jk(e, o) : Jm(e, o);
      if (f !== Lo) {
        if (f === ec) {
          var p = zl(e);
          p !== Z && (o = p, f = uS(e, p));
        }
        if (f === Qp) {
          var v = qp;
          throw nc(e, Z), Xu(e, o), ti(e, wn()), v;
        }
        if (f === eS)
          Xu(e, o);
        else {
          var g = !ks(e, o), x = e.current.alternate;
          if (g && !Tk(x)) {
            if (f = Jm(e, o), f === ec) {
              var N = zl(e);
              N !== Z && (o = N, f = uS(e, N));
            }
            if (f === Qp) {
              var _ = qp;
              throw nc(e, Z), Xu(e, o), ti(e, wn()), _;
            }
          }
          e.finishedWork = x, e.finishedLanes = o, Rk(e, f, o);
        }
      }
      return ti(e, wn()), e.callbackNode === a ? kC.bind(null, e) : null;
    }
    function uS(e, t) {
      var a = Kp;
      if (af(e)) {
        var i = nc(e, t);
        i.flags |= _n, Yw(e.containerInfo);
      }
      var o = Jm(e, t);
      if (o !== ec) {
        var s = ei;
        ei = a, s !== null && _C(s);
      }
      return o;
    }
    function _C(e) {
      ei === null ? ei = e : ei.push.apply(ei, e);
    }
    function Rk(e, t, a) {
      switch (t) {
        case Lo:
        case Qp:
          throw new Error("Root did not complete. This is a bug in React.");
        case ec: {
          rc(e, ei, jo);
          break;
        }
        case $m: {
          if (Xu(e, a), ah(a) && // do not delay if we're inside an act() scope
          !$C()) {
            var i = nS + EC - wn();
            if (i > 10) {
              var o = yo(e, Z);
              if (o !== Z)
                break;
              var s = e.suspendedLanes;
              if (!go(s, a)) {
                Na(), tf(e, s);
                break;
              }
              e.timeoutHandle = ig(rc.bind(null, e, ei, jo), i);
              break;
            }
          }
          rc(e, ei, jo);
          break;
        }
        case Gp: {
          if (Xu(e, a), lh(a))
            break;
          if (!$C()) {
            var f = th(e, a), p = f, v = wn() - p, g = Yk(v) - v;
            if (g > 10) {
              e.timeoutHandle = ig(rc.bind(null, e, ei, jo), g);
              break;
            }
          }
          rc(e, ei, jo);
          break;
        }
        case CC: {
          rc(e, ei, jo);
          break;
        }
        default:
          throw new Error("Unknown root exit status.");
      }
    }
    function Tk(e) {
      for (var t = e; ; ) {
        if (t.flags & ys) {
          var a = t.updateQueue;
          if (a !== null) {
            var i = a.stores;
            if (i !== null)
              for (var o = 0; o < i.length; o++) {
                var s = i[o], f = s.getSnapshot, p = s.value;
                try {
                  if (!De(f(), p))
                    return !1;
                } catch {
                  return !1;
                }
              }
          }
        }
        var v = t.child;
        if (t.subtreeFlags & ys && v !== null) {
          v.return = t, t = v;
          continue;
        }
        if (t === e)
          return !0;
        for (; t.sibling === null; ) {
          if (t.return === null || t.return === e)
            return !0;
          t = t.return;
        }
        t.sibling.return = t.return, t = t.sibling;
      }
      return !0;
    }
    function Xu(e, t) {
      t = _s(t, Ym), t = _s(t, Xp), ch(e, t);
    }
    function DC(e) {
      if ($R(), (Ft & (Wr | zi)) !== yr)
        throw new Error("Should not already be working.");
      Ao();
      var t = yo(e, Z);
      if (!ca(t, Qe))
        return ti(e, wn()), null;
      var a = Jm(e, t);
      if (e.tag !== Fu && a === ec) {
        var i = zl(e);
        i !== Z && (t = i, a = uS(e, i));
      }
      if (a === Qp) {
        var o = qp;
        throw nc(e, Z), Xu(e, t), ti(e, wn()), o;
      }
      if (a === eS)
        throw new Error("Root did not complete. This is a bug in React.");
      var s = e.current.alternate;
      return e.finishedWork = s, e.finishedLanes = t, rc(e, ei, jo), ti(e, wn()), null;
    }
    function kk(e, t) {
      t !== Z && (Yd(e, gt(t, Qe)), ti(e, wn()), (Ft & (Wr | zi)) === yr && (Jp(), Hu()));
    }
    function sS(e, t) {
      var a = Ft;
      Ft |= bC;
      try {
        return e(t);
      } finally {
        Ft = a, Ft === yr && // Treat `act` as if it's inside `batchedUpdates`, even in legacy mode.
        !dl.isBatchingLegacy && (Jp(), Tx());
      }
    }
    function _k(e, t, a, i, o) {
      var s = Wa(), f = Yr.transition;
      try {
        return Yr.transition = null, Dn(zn), e(t, a, i, o);
      } finally {
        Dn(s), Yr.transition = f, Ft === yr && Jp();
      }
    }
    function zo(e) {
      Gu !== null && Gu.tag === Fu && (Ft & (Wr | zi)) === yr && Ao();
      var t = Ft;
      Ft |= bC;
      var a = Yr.transition, i = Wa();
      try {
        return Yr.transition = null, Dn(zn), e ? e() : void 0;
      } finally {
        Dn(i), Yr.transition = a, Ft = t, (Ft & (Wr | zi)) === yr && Hu();
      }
    }
    function NC() {
      return (Ft & (Wr | zi)) !== yr;
    }
    function Km(e, t) {
      pa(tS, ql, e), ql = gt(ql, t);
    }
    function cS(e) {
      ql = tS.current, da(tS, e);
    }
    function nc(e, t) {
      e.finishedWork = null, e.finishedLanes = Z;
      var a = e.timeoutHandle;
      if (a !== lg && (e.timeoutHandle = lg, tw(a)), Un !== null)
        for (var i = Un.return; i !== null; ) {
          var o = i.alternate;
          iC(o, i), i = i.return;
        }
      Da = e;
      var s = ac(e.current, null);
      return Un = s, gr = ql = t, Sr = Lo, qp = null, Im = Z, Xp = Z, Ym = Z, Kp = null, ei = null, ER(), al.discardPendingWarnings(), s;
    }
    function OC(e, t) {
      do {
        var a = Un;
        try {
          if (om(), tb(), kn(), Z0.current = null, a === null || a.return === null) {
            Sr = Qp, qp = t, Un = null;
            return;
          }
          if (vt && a.mode & ut && Am(a, !0), ft)
            if (oa(), t !== null && typeof t == "object" && typeof t.then == "function") {
              var i = t;
              fo(a, i, gr);
            } else
              xs(a, t, gr);
          JR(e, a.return, a, t, gr), zC(a);
        } catch (o) {
          t = o, Un === a && a !== null ? (a = a.return, Un = a) : a = Un;
          continue;
        }
        return;
      } while (!0);
    }
    function MC() {
      var e = J0.current;
      return J0.current = Om, e === null ? Om : e;
    }
    function LC(e) {
      J0.current = e;
    }
    function Dk() {
      nS = wn();
    }
    function nv(e) {
      Im = gt(e, Im);
    }
    function Nk() {
      Sr === Lo && (Sr = $m);
    }
    function fS() {
      (Sr === Lo || Sr === $m || Sr === ec) && (Sr = Gp), Da !== null && (Ts(Im) || Ts(Xp)) && Xu(Da, gr);
    }
    function Ok(e) {
      Sr !== Gp && (Sr = ec), Kp === null ? Kp = [e] : Kp.push(e);
    }
    function Mk() {
      return Sr === Lo;
    }
    function Jm(e, t) {
      var a = Ft;
      Ft |= Wr;
      var i = MC();
      if (Da !== e || gr !== t) {
        if (Ra) {
          var o = e.memoizedUpdaters;
          o.size > 0 && (rv(e, gr), o.clear()), Wd(e, t);
        }
        jo = Ns(), nc(e, t);
      }
      gn(t);
      do
        try {
          Lk();
          break;
        } catch (s) {
          OC(e, s);
        }
      while (!0);
      if (om(), Ft = a, LC(i), Un !== null)
        throw new Error("Cannot commit an incomplete root. This error is likely caused by a bug in React. Please file an issue.");
      return Ac(), Da = null, gr = Z, Sr;
    }
    function Lk() {
      for (; Un !== null; )
        jC(Un);
    }
    function jk(e, t) {
      var a = Ft;
      Ft |= Wr;
      var i = MC();
      if (Da !== e || gr !== t) {
        if (Ra) {
          var o = e.memoizedUpdaters;
          o.size > 0 && (rv(e, gr), o.clear()), Wd(e, t);
        }
        jo = Ns(), Jp(), nc(e, t);
      }
      gn(t);
      do
        try {
          zk();
          break;
        } catch (s) {
          OC(e, s);
        }
      while (!0);
      return om(), LC(i), Ft = a, Un !== null ? (zc(), Lo) : (Ac(), Da = null, gr = Z, Sr);
    }
    function zk() {
      for (; Un !== null && !Dc(); )
        jC(Un);
    }
    function jC(e) {
      var t = e.alternate;
      Jt(e);
      var a;
      (e.mode & ut) !== Fe ? (v0(e), a = dS(t, e, ql), Am(e, !0)) : a = dS(t, e, ql), kn(), e.memoizedProps = e.pendingProps, a === null ? zC(e) : Un = a, Z0.current = null;
    }
    function zC(e) {
      var t = e;
      do {
        var a = t.alternate, i = t.return;
        if ((t.flags & Ca) === qe) {
          Jt(t);
          var o = void 0;
          if ((t.mode & ut) === Fe ? o = aC(a, t, ql) : (v0(t), o = aC(a, t, ql), Am(t, !1)), kn(), o !== null) {
            Un = o;
            return;
          }
        } else {
          var s = NT(a, t);
          if (s !== null) {
            s.flags &= Iv, Un = s;
            return;
          }
          if ((t.mode & ut) !== Fe) {
            Am(t, !1);
            for (var f = t.actualDuration, p = t.child; p !== null; )
              f += p.actualDuration, p = p.sibling;
            t.actualDuration = f;
          }
          if (i !== null)
            i.flags |= Ca, i.subtreeFlags = qe, i.deletions = null;
          else {
            Sr = eS, Un = null;
            return;
          }
        }
        var v = t.sibling;
        if (v !== null) {
          Un = v;
          return;
        }
        t = i, Un = t;
      } while (t !== null);
      Sr === Lo && (Sr = CC);
    }
    function rc(e, t, a) {
      var i = Wa(), o = Yr.transition;
      try {
        Yr.transition = null, Dn(zn), Ak(e, t, a, i);
      } finally {
        Yr.transition = o, Dn(i);
      }
      return null;
    }
    function Ak(e, t, a, i) {
      do
        Ao();
      while (Gu !== null);
      if (Qk(), (Ft & (Wr | zi)) !== yr)
        throw new Error("Should not already be working.");
      var o = e.finishedWork, s = e.finishedLanes;
      if (Ml(s), o === null)
        return Mc(), null;
      if (s === Z && y("root.finishedLanes should not be empty during a commit. This is a bug in React."), e.finishedWork = null, e.finishedLanes = Z, o === e.current)
        throw new Error("Cannot commit the same tree as before. This error is likely caused by a bug in React. Please file an issue.");
      e.callbackNode = null, e.callbackPriority = $n;
      var f = gt(o.lanes, o.childLanes);
      nf(e, f), e === Da && (Da = null, Un = null, gr = Z), ((o.subtreeFlags & Va) !== qe || (o.flags & Va) !== qe) && (tc || (tc = !0, iS = a, hS(Ri, function() {
        return Ao(), null;
      })));
      var p = (o.subtreeFlags & (iu | ia | Tr | Va)) !== qe, v = (o.flags & (iu | ia | Tr | Va)) !== qe;
      if (p || v) {
        var g = Yr.transition;
        Yr.transition = null;
        var x = Wa();
        Dn(zn);
        var N = Ft;
        Ft |= zi, Z0.current = null, zT(e, o), Tb(), qT(e, o, s), G1(e.containerInfo), e.current = o, Ud(s), XT(o, e, s), cu(), Qv(), Ft = N, Dn(x), Yr.transition = g;
      } else
        e.current = o, Tb();
      var _ = tc;
      if (tc ? (tc = !1, Gu = e, Zp = s) : (Kf = 0, Gm = null), f = e.pendingLanes, f === Z && (Xf = null), _ || HC(e.current, !1), ou(o.stateNode, i), Ra && e.memoizedUpdaters.clear(), hk(), ti(e, wn()), t !== null)
        for (var A = e.onRecoverableError, P = 0; P < t.length; P++) {
          var Q = t[P], ge = Q.stack, Xe = Q.digest;
          A(Q.value, {
            componentStack: ge,
            digest: Xe
          });
        }
      if (Wm) {
        Wm = !1;
        var Be = rS;
        throw rS = null, Be;
      }
      return ca(Zp, Qe) && e.tag !== Fu && Ao(), f = e.pendingLanes, ca(f, Qe) ? (VR(), e === lS ? ev++ : (ev = 0, lS = e)) : ev = 0, Hu(), Mc(), null;
    }
    function Ao() {
      if (Gu !== null) {
        var e = dr(Zp), t = Ny(Ti, e), a = Yr.transition, i = Wa();
        try {
          return Yr.transition = null, Dn(t), Fk();
        } finally {
          Dn(i), Yr.transition = a;
        }
      }
      return !1;
    }
    function Uk(e) {
      aS.push(e), tc || (tc = !0, hS(Ri, function() {
        return Ao(), null;
      }));
    }
    function Fk() {
      if (Gu === null)
        return !1;
      var e = iS;
      iS = null;
      var t = Gu, a = Zp;
      if (Gu = null, Zp = Z, (Ft & (Wr | zi)) !== yr)
        throw new Error("Cannot flush passive effects while already rendering.");
      oS = !0, Qm = !1, Zv(a);
      var i = Ft;
      Ft |= zi, rk(t.current), ZT(t, t.current, a, e);
      {
        var o = aS;
        aS = [];
        for (var s = 0; s < o.length; s++) {
          var f = o[s];
          HT(t, f);
        }
      }
      Fd(), HC(t.current, !0), Ft = i, Hu(), Qm ? t === Gm ? Kf++ : (Kf = 0, Gm = t) : Kf = 0, oS = !1, Qm = !1, Ia(t);
      {
        var p = t.current.stateNode;
        p.effectDuration = 0, p.passiveEffectDuration = 0;
      }
      return !0;
    }
    function AC(e) {
      return Xf !== null && Xf.has(e);
    }
    function Hk(e) {
      Xf === null ? Xf = /* @__PURE__ */ new Set([e]) : Xf.add(e);
    }
    function Pk(e) {
      Wm || (Wm = !0, rS = e);
    }
    var Vk = Pk;
    function UC(e, t, a) {
      var i = Js(a, t), o = jb(e, i, Qe), s = Vu(e, o, Qe), f = Na();
      s !== null && (So(s, Qe, f), ti(s, f));
    }
    function mn(e, t, a) {
      if (MT(a), av(!1), e.tag === ne) {
        UC(e, e, a);
        return;
      }
      var i = null;
      for (i = t; i !== null; ) {
        if (i.tag === ne) {
          UC(i, e, a);
          return;
        } else if (i.tag === K) {
          var o = i.type, s = i.stateNode;
          if (typeof o.getDerivedStateFromError == "function" || typeof s.componentDidCatch == "function" && !AC(s)) {
            var f = Js(a, e), p = M0(i, f, Qe), v = Vu(i, p, Qe), g = Na();
            v !== null && (So(v, Qe, g), ti(v, g));
            return;
          }
        }
        i = i.return;
      }
      y(`Internal React error: Attempted to capture a commit phase error inside a detached tree. This indicates a bug in React. Likely causes include deleting the same fiber more than once, committing an already-finished tree, or an inconsistent return pointer.

Error message:

%s`, a);
    }
    function Bk(e, t, a) {
      var i = e.pingCache;
      i !== null && i.delete(t);
      var o = Na();
      tf(e, a), Kk(e), Da === e && go(gr, a) && (Sr === Gp || Sr === $m && ah(gr) && wn() - nS < EC ? nc(e, Z) : Ym = gt(Ym, a)), ti(e, o);
    }
    function FC(e, t) {
      t === $n && (t = Ck(e));
      var a = Na(), i = Ja(e, t);
      i !== null && (So(i, t, a), ti(i, a));
    }
    function $k(e) {
      var t = e.memoizedState, a = $n;
      t !== null && (a = t.retryLane), FC(e, a);
    }
    function Ik(e, t) {
      var a = $n, i;
      switch (e.tag) {
        case ke:
          i = e.stateNode;
          var o = e.memoizedState;
          o !== null && (a = o.retryLane);
          break;
        case it:
          i = e.stateNode;
          break;
        default:
          throw new Error("Pinged unknown suspense boundary type. This is probably a bug in React.");
      }
      i !== null && i.delete(t), FC(e, a);
    }
    function Yk(e) {
      return e < 120 ? 120 : e < 480 ? 480 : e < 1080 ? 1080 : e < 1920 ? 1920 : e < 3e3 ? 3e3 : e < 4320 ? 4320 : gk(e / 1960) * 1960;
    }
    function Wk() {
      if (ev > xk)
        throw ev = 0, lS = null, new Error("Maximum update depth exceeded. This can happen when a component repeatedly calls setState inside componentWillUpdate or componentDidUpdate. React limits the number of nested updates to prevent infinite loops.");
      Kf > bk && (Kf = 0, Gm = null, y("Maximum update depth exceeded. This can happen when a component calls setState inside useEffect, but useEffect either doesn't have a dependency array, or one of the dependencies changes on every render."));
    }
    function Qk() {
      al.flushLegacyContextWarning(), al.flushPendingUnsafeLifecycleWarnings();
    }
    function HC(e, t) {
      Jt(e), Zm(e, aa, dk), t && Zm(e, uo, pk), Zm(e, aa, ck), t && Zm(e, uo, fk), kn();
    }
    function Zm(e, t, a) {
      for (var i = e, o = null; i !== null; ) {
        var s = i.subtreeFlags & t;
        i !== o && i.child !== null && s !== qe ? i = i.child : ((i.flags & t) !== qe && a(i), i.sibling !== null ? i = i.sibling : i = o = i.return);
      }
    }
    var ey = null;
    function PC(e) {
      {
        if ((Ft & Wr) !== yr || !(e.mode & Ve))
          return;
        var t = e.tag;
        if (t !== ye && t !== ne && t !== K && t !== B && t !== Ke && t !== at && t !== Ye)
          return;
        var a = dt(e) || "ReactComponent";
        if (ey !== null) {
          if (ey.has(a))
            return;
          ey.add(a);
        } else
          ey = /* @__PURE__ */ new Set([a]);
        var i = En;
        try {
          Jt(e), y("Can't perform a React state update on a component that hasn't mounted yet. This indicates that you have a side-effect in your render function that asynchronously later calls tries to update the component. Move this work to useEffect instead.");
        } finally {
          i ? Jt(e) : kn();
        }
      }
    }
    var dS;
    {
      var Gk = null;
      dS = function(e, t, a) {
        var i = GC(Gk, t);
        try {
          return Zb(e, t, a);
        } catch (s) {
          if (lR() || s !== null && typeof s == "object" && typeof s.then == "function")
            throw s;
          if (om(), tb(), iC(e, t), GC(t, i), t.mode & ut && v0(t), oo(null, Zb, null, e, t, a), Ry()) {
            var o = _d();
            typeof o == "object" && o !== null && o._suppressLogging && typeof s == "object" && s !== null && !s._suppressLogging && (s._suppressLogging = !0);
          }
          throw s;
        }
      };
    }
    var VC = !1, pS;
    pS = /* @__PURE__ */ new Set();
    function qk(e) {
      if (Zr && !FR())
        switch (e.tag) {
          case B:
          case Ke:
          case Ye: {
            var t = Un && dt(Un) || "Unknown", a = t;
            if (!pS.has(a)) {
              pS.add(a);
              var i = dt(e) || "Unknown";
              y("Cannot update a component (`%s`) while rendering a different component (`%s`). To locate the bad setState() call inside `%s`, follow the stack trace as described in https://reactjs.org/link/setstate-in-render", i, t, t);
            }
            break;
          }
          case K: {
            VC || (y("Cannot update during an existing state transition (such as within `render`). Render methods should be a pure function of props and state."), VC = !0);
            break;
          }
        }
    }
    function rv(e, t) {
      if (Ra) {
        var a = e.memoizedUpdaters;
        a.forEach(function(i) {
          rf(e, i, t);
        });
      }
    }
    var vS = {};
    function hS(e, t) {
      {
        var a = dl.current;
        return a !== null ? (a.push(t), vS) : _c(e, t);
      }
    }
    function BC(e) {
      if (e !== vS)
        return Wv(e);
    }
    function $C() {
      return dl.current !== null;
    }
    function Xk(e) {
      {
        if (e.mode & Ve) {
          if (!xC())
            return;
        } else if (!yk() || Ft !== yr || e.tag !== B && e.tag !== Ke && e.tag !== Ye)
          return;
        if (dl.current === null) {
          var t = En;
          try {
            Jt(e), y(`An update to %s inside a test was not wrapped in act(...).

When testing, code that causes React state updates should be wrapped into act(...):

act(() => {
  /* fire events that update state */
});
/* assert on the output */

This ensures that you're testing the behavior the user would see in the browser. Learn more at https://reactjs.org/link/wrap-tests-with-act`, dt(e));
          } finally {
            t ? Jt(e) : kn();
          }
        }
      }
    }
    function Kk(e) {
      e.tag !== Fu && xC() && dl.current === null && y(`A suspended resource finished loading inside a test, but the event was not wrapped in act(...).

When testing, code that resolves suspended data should be wrapped into act(...):

act(() => {
  /* finish loading suspended data */
});
/* assert on the output */

This ensures that you're testing the behavior the user would see in the browser. Learn more at https://reactjs.org/link/wrap-tests-with-act`);
    }
    function av(e) {
      TC = e;
    }
    var Ai = null, Jf = null, Jk = function(e) {
      Ai = e;
    };
    function Zf(e) {
      {
        if (Ai === null)
          return e;
        var t = Ai(e);
        return t === void 0 ? e : t.current;
      }
    }
    function mS(e) {
      return Zf(e);
    }
    function yS(e) {
      {
        if (Ai === null)
          return e;
        var t = Ai(e);
        if (t === void 0) {
          if (e != null && typeof e.render == "function") {
            var a = Zf(e.render);
            if (e.render !== a) {
              var i = {
                $$typeof: ie,
                render: a
              };
              return e.displayName !== void 0 && (i.displayName = e.displayName), i;
            }
          }
          return e;
        }
        return t.current;
      }
    }
    function IC(e, t) {
      {
        if (Ai === null)
          return !1;
        var a = e.elementType, i = t.type, o = !1, s = typeof i == "object" && i !== null ? i.$$typeof : null;
        switch (e.tag) {
          case K: {
            typeof i == "function" && (o = !0);
            break;
          }
          case B: {
            (typeof i == "function" || s === Ze) && (o = !0);
            break;
          }
          case Ke: {
            (s === ie || s === Ze) && (o = !0);
            break;
          }
          case at:
          case Ye: {
            (s === jt || s === Ze) && (o = !0);
            break;
          }
          default:
            return !1;
        }
        if (o) {
          var f = Ai(a);
          if (f !== void 0 && f === Ai(i))
            return !0;
        }
        return !1;
      }
    }
    function YC(e) {
      {
        if (Ai === null || typeof WeakSet != "function")
          return;
        Jf === null && (Jf = /* @__PURE__ */ new WeakSet()), Jf.add(e);
      }
    }
    var Zk = function(e, t) {
      {
        if (Ai === null)
          return;
        var a = t.staleFamilies, i = t.updatedFamilies;
        Ao(), zo(function() {
          gS(e.current, i, a);
        });
      }
    }, e_ = function(e, t) {
      {
        if (e.context !== pi)
          return;
        Ao(), zo(function() {
          iv(t, e, null, null);
        });
      }
    };
    function gS(e, t, a) {
      {
        var i = e.alternate, o = e.child, s = e.sibling, f = e.tag, p = e.type, v = null;
        switch (f) {
          case B:
          case Ye:
          case K:
            v = p;
            break;
          case Ke:
            v = p.render;
            break;
        }
        if (Ai === null)
          throw new Error("Expected resolveFamily to be set during hot reload.");
        var g = !1, x = !1;
        if (v !== null) {
          var N = Ai(v);
          N !== void 0 && (a.has(N) ? x = !0 : t.has(N) && (f === K ? x = !0 : g = !0));
        }
        if (Jf !== null && (Jf.has(e) || i !== null && Jf.has(i)) && (x = !0), x && (e._debugNeedsRemount = !0), x || g) {
          var _ = Ja(e, Qe);
          _ !== null && xr(_, e, Qe, fn);
        }
        o !== null && !x && gS(o, t, a), s !== null && gS(s, t, a);
      }
    }
    var t_ = function(e, t) {
      {
        var a = /* @__PURE__ */ new Set(), i = new Set(t.map(function(o) {
          return o.current;
        }));
        return SS(e.current, i, a), a;
      }
    };
    function SS(e, t, a) {
      {
        var i = e.child, o = e.sibling, s = e.tag, f = e.type, p = null;
        switch (s) {
          case B:
          case Ye:
          case K:
            p = f;
            break;
          case Ke:
            p = f.render;
            break;
        }
        var v = !1;
        p !== null && t.has(p) && (v = !0), v ? n_(e, a) : i !== null && SS(i, t, a), o !== null && SS(o, t, a);
      }
    }
    function n_(e, t) {
      {
        var a = r_(e, t);
        if (a)
          return;
        for (var i = e; ; ) {
          switch (i.tag) {
            case V:
              t.add(i.stateNode);
              return;
            case oe:
              t.add(i.stateNode.containerInfo);
              return;
            case ne:
              t.add(i.stateNode.containerInfo);
              return;
          }
          if (i.return === null)
            throw new Error("Expected to reach root first.");
          i = i.return;
        }
      }
    }
    function r_(e, t) {
      for (var a = e, i = !1; ; ) {
        if (a.tag === V)
          i = !0, t.add(a.stateNode);
        else if (a.child !== null) {
          a.child.return = a, a = a.child;
          continue;
        }
        if (a === e)
          return i;
        for (; a.sibling === null; ) {
          if (a.return === null || a.return === e)
            return i;
          a = a.return;
        }
        a.sibling.return = a.return, a = a.sibling;
      }
      return !1;
    }
    var xS;
    {
      xS = !1;
      try {
        var WC = Object.preventExtensions({});
      } catch {
        xS = !0;
      }
    }
    function a_(e, t, a, i) {
      this.tag = e, this.key = a, this.elementType = null, this.type = null, this.stateNode = null, this.return = null, this.child = null, this.sibling = null, this.index = 0, this.ref = null, this.pendingProps = t, this.memoizedProps = null, this.updateQueue = null, this.memoizedState = null, this.dependencies = null, this.mode = i, this.flags = qe, this.subtreeFlags = qe, this.deletions = null, this.lanes = Z, this.childLanes = Z, this.alternate = null, this.actualDuration = Number.NaN, this.actualStartTime = Number.NaN, this.selfBaseDuration = Number.NaN, this.treeBaseDuration = Number.NaN, this.actualDuration = 0, this.actualStartTime = -1, this.selfBaseDuration = 0, this.treeBaseDuration = 0, this._debugSource = null, this._debugOwner = null, this._debugNeedsRemount = !1, this._debugHookTypes = null, !xS && typeof Object.preventExtensions == "function" && Object.preventExtensions(this);
    }
    var vi = function(e, t, a, i) {
      return new a_(e, t, a, i);
    };
    function bS(e) {
      var t = e.prototype;
      return !!(t && t.isReactComponent);
    }
    function i_(e) {
      return typeof e == "function" && !bS(e) && e.defaultProps === void 0;
    }
    function l_(e) {
      if (typeof e == "function")
        return bS(e) ? K : B;
      if (e != null) {
        var t = e.$$typeof;
        if (t === ie)
          return Ke;
        if (t === jt)
          return at;
      }
      return ye;
    }
    function ac(e, t) {
      var a = e.alternate;
      a === null ? (a = vi(e.tag, t, e.key, e.mode), a.elementType = e.elementType, a.type = e.type, a.stateNode = e.stateNode, a._debugSource = e._debugSource, a._debugOwner = e._debugOwner, a._debugHookTypes = e._debugHookTypes, a.alternate = e, e.alternate = a) : (a.pendingProps = t, a.type = e.type, a.flags = qe, a.subtreeFlags = qe, a.deletions = null, a.actualDuration = 0, a.actualStartTime = -1), a.flags = e.flags & cr, a.childLanes = e.childLanes, a.lanes = e.lanes, a.child = e.child, a.memoizedProps = e.memoizedProps, a.memoizedState = e.memoizedState, a.updateQueue = e.updateQueue;
      var i = e.dependencies;
      switch (a.dependencies = i === null ? null : {
        lanes: i.lanes,
        firstContext: i.firstContext
      }, a.sibling = e.sibling, a.index = e.index, a.ref = e.ref, a.selfBaseDuration = e.selfBaseDuration, a.treeBaseDuration = e.treeBaseDuration, a._debugNeedsRemount = e._debugNeedsRemount, a.tag) {
        case ye:
        case B:
        case Ye:
          a.type = Zf(e.type);
          break;
        case K:
          a.type = mS(e.type);
          break;
        case Ke:
          a.type = yS(e.type);
          break;
      }
      return a;
    }
    function o_(e, t) {
      e.flags &= cr | pn;
      var a = e.alternate;
      if (a === null)
        e.childLanes = Z, e.lanes = t, e.child = null, e.subtreeFlags = qe, e.memoizedProps = null, e.memoizedState = null, e.updateQueue = null, e.dependencies = null, e.stateNode = null, e.selfBaseDuration = 0, e.treeBaseDuration = 0;
      else {
        e.childLanes = a.childLanes, e.lanes = a.lanes, e.child = a.child, e.subtreeFlags = qe, e.deletions = null, e.memoizedProps = a.memoizedProps, e.memoizedState = a.memoizedState, e.updateQueue = a.updateQueue, e.type = a.type;
        var i = a.dependencies;
        e.dependencies = i === null ? null : {
          lanes: i.lanes,
          firstContext: i.firstContext
        }, e.selfBaseDuration = a.selfBaseDuration, e.treeBaseDuration = a.treeBaseDuration;
      }
      return e;
    }
    function u_(e, t, a) {
      var i;
      return e === Kh ? (i = Ve, t === !0 && (i |= _t, i |= Ta)) : i = Fe, Ra && (i |= ut), vi(ne, null, null, i);
    }
    function CS(e, t, a, i, o, s) {
      var f = ye, p = e;
      if (typeof e == "function")
        bS(e) ? (f = K, p = mS(p)) : p = Zf(p);
      else if (typeof e == "string")
        f = V;
      else
        e:
          switch (e) {
            case ba:
              return Ku(a.children, o, s, t);
            case gi:
              f = Ae, o |= _t, (o & Ve) !== Fe && (o |= Ta);
              break;
            case Si:
              return s_(a, o, s, t);
            case Pe:
              return c_(a, o, s, t);
            case Tt:
              return f_(a, o, s, t);
            case ln:
              return QC(a, o, s, t);
            case dn:
            case Ct:
            case Rr:
            case xi:
            case Pn:
            default: {
              if (typeof e == "object" && e !== null)
                switch (e.$$typeof) {
                  case T:
                    f = rt;
                    break e;
                  case ee:
                    f = Dt;
                    break e;
                  case ie:
                    f = Ke, p = yS(p);
                    break e;
                  case jt:
                    f = at;
                    break e;
                  case Ze:
                    f = be, p = null;
                    break e;
                }
              var v = "";
              {
                (e === void 0 || typeof e == "object" && e !== null && Object.keys(e).length === 0) && (v += " You likely forgot to export your component from the file it's defined in, or you might have mixed up default and named imports.");
                var g = i ? dt(i) : null;
                g && (v += `

Check the render method of \`` + g + "`.");
              }
              throw new Error("Element type is invalid: expected a string (for built-in components) or a class/function (for composite components) " + ("but got: " + (e == null ? e : typeof e) + "." + v));
            }
          }
      var x = vi(f, a, t, o);
      return x.elementType = e, x.type = p, x.lanes = s, x._debugOwner = i, x;
    }
    function ES(e, t, a) {
      var i = null;
      i = e._owner;
      var o = e.type, s = e.key, f = e.props, p = CS(o, s, f, i, t, a);
      return p._debugSource = e._source, p._debugOwner = e._owner, p;
    }
    function Ku(e, t, a, i) {
      var o = vi(de, e, i, t);
      return o.lanes = a, o;
    }
    function s_(e, t, a, i) {
      typeof e.id != "string" && y('Profiler must specify an "id" of type `string` as a prop. Received the type `%s` instead.', typeof e.id);
      var o = vi(ct, e, i, t | ut);
      return o.elementType = Si, o.lanes = a, o.stateNode = {
        effectDuration: 0,
        passiveEffectDuration: 0
      }, o;
    }
    function c_(e, t, a, i) {
      var o = vi(ke, e, i, t);
      return o.elementType = Pe, o.lanes = a, o;
    }
    function f_(e, t, a, i) {
      var o = vi(it, e, i, t);
      return o.elementType = Tt, o.lanes = a, o;
    }
    function QC(e, t, a, i) {
      var o = vi(Ie, e, i, t);
      o.elementType = ln, o.lanes = a;
      var s = {
        isHidden: !1
      };
      return o.stateNode = s, o;
    }
    function wS(e, t, a) {
      var i = vi($, e, null, t);
      return i.lanes = a, i;
    }
    function d_() {
      var e = vi(V, null, null, Fe);
      return e.elementType = "DELETED", e;
    }
    function p_(e) {
      var t = vi($e, null, null, Fe);
      return t.stateNode = e, t;
    }
    function RS(e, t, a) {
      var i = e.children !== null ? e.children : [], o = vi(oe, i, e.key, t);
      return o.lanes = a, o.stateNode = {
        containerInfo: e.containerInfo,
        pendingChildren: null,
        // Used by persistent updates
        implementation: e.implementation
      }, o;
    }
    function GC(e, t) {
      return e === null && (e = vi(ye, null, null, Fe)), e.tag = t.tag, e.key = t.key, e.elementType = t.elementType, e.type = t.type, e.stateNode = t.stateNode, e.return = t.return, e.child = t.child, e.sibling = t.sibling, e.index = t.index, e.ref = t.ref, e.pendingProps = t.pendingProps, e.memoizedProps = t.memoizedProps, e.updateQueue = t.updateQueue, e.memoizedState = t.memoizedState, e.dependencies = t.dependencies, e.mode = t.mode, e.flags = t.flags, e.subtreeFlags = t.subtreeFlags, e.deletions = t.deletions, e.lanes = t.lanes, e.childLanes = t.childLanes, e.alternate = t.alternate, e.actualDuration = t.actualDuration, e.actualStartTime = t.actualStartTime, e.selfBaseDuration = t.selfBaseDuration, e.treeBaseDuration = t.treeBaseDuration, e._debugSource = t._debugSource, e._debugOwner = t._debugOwner, e._debugNeedsRemount = t._debugNeedsRemount, e._debugHookTypes = t._debugHookTypes, e;
    }
    function v_(e, t, a, i, o) {
      this.tag = t, this.containerInfo = e, this.pendingChildren = null, this.current = null, this.pingCache = null, this.finishedWork = null, this.timeoutHandle = lg, this.context = null, this.pendingContext = null, this.callbackNode = null, this.callbackPriority = $n, this.eventTimes = Ds(Z), this.expirationTimes = Ds(fn), this.pendingLanes = Z, this.suspendedLanes = Z, this.pingedLanes = Z, this.expiredLanes = Z, this.mutableReadLanes = Z, this.finishedLanes = Z, this.entangledLanes = Z, this.entanglements = Ds(Z), this.identifierPrefix = i, this.onRecoverableError = o, this.mutableSourceEagerHydrationData = null, this.effectDuration = 0, this.passiveEffectDuration = 0;
      {
        this.memoizedUpdaters = /* @__PURE__ */ new Set();
        for (var s = this.pendingUpdatersLaneMap = [], f = 0; f < Es; f++)
          s.push(/* @__PURE__ */ new Set());
      }
      switch (t) {
        case Kh:
          this._debugRootType = a ? "hydrateRoot()" : "createRoot()";
          break;
        case Fu:
          this._debugRootType = a ? "hydrate()" : "render()";
          break;
      }
    }
    function qC(e, t, a, i, o, s, f, p, v, g) {
      var x = new v_(e, t, a, p, v), N = u_(t, s);
      x.current = N, N.stateNode = x;
      {
        var _ = {
          element: i,
          isDehydrated: a,
          cache: null,
          // not enabled yet
          transitions: null,
          pendingSuspenseBoundaries: null
        };
        N.memoizedState = _;
      }
      return Fg(N), x;
    }
    var TS = "18.3.1";
    function h_(e, t, a) {
      var i = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : null;
      return qr(i), {
        // This tag allow us to uniquely identify this as a React Portal
        $$typeof: Lr,
        key: i == null ? null : "" + i,
        children: e,
        containerInfo: t,
        implementation: a
      };
    }
    var kS, _S;
    kS = !1, _S = {};
    function XC(e) {
      if (!e)
        return pi;
      var t = Fa(e), a = Kw(t);
      if (t.tag === K) {
        var i = t.type;
        if (Bl(i))
          return Ex(t, i, a);
      }
      return a;
    }
    function m_(e, t) {
      {
        var a = Fa(e);
        if (a === void 0) {
          if (typeof e.render == "function")
            throw new Error("Unable to find node on an unmounted component.");
          var i = Object.keys(e).join(",");
          throw new Error("Argument appears to not be a ReactComponent. Keys: " + i);
        }
        var o = Ba(a);
        if (o === null)
          return null;
        if (o.mode & _t) {
          var s = dt(a) || "Component";
          if (!_S[s]) {
            _S[s] = !0;
            var f = En;
            try {
              Jt(o), a.mode & _t ? y("%s is deprecated in StrictMode. %s was passed an instance of %s which is inside StrictMode. Instead, add a ref directly to the element you want to reference. Learn more about using refs safely here: https://reactjs.org/link/strict-mode-find-node", t, t, s) : y("%s is deprecated in StrictMode. %s was passed an instance of %s which renders StrictMode children. Instead, add a ref directly to the element you want to reference. Learn more about using refs safely here: https://reactjs.org/link/strict-mode-find-node", t, t, s);
            } finally {
              f ? Jt(f) : kn();
            }
          }
        }
        return o.stateNode;
      }
    }
    function KC(e, t, a, i, o, s, f, p) {
      var v = !1, g = null;
      return qC(e, t, v, g, a, i, o, s, f);
    }
    function JC(e, t, a, i, o, s, f, p, v, g) {
      var x = !0, N = qC(a, i, x, e, o, s, f, p, v);
      N.context = XC(null);
      var _ = N.current, A = Na(), P = qu(_), Q = Oo(A, P);
      return Q.callback = t ?? null, Vu(_, Q, P), Ek(N, P, A), N;
    }
    function iv(e, t, a, i) {
      Ad(t, e);
      var o = t.current, s = Na(), f = qu(o);
      Hd(f);
      var p = XC(a);
      t.context === null ? t.context = p : t.pendingContext = p, Zr && En !== null && !kS && (kS = !0, y(`Render methods should be a pure function of props and state; triggering nested component updates from render is not allowed. If necessary, trigger nested updates in componentDidUpdate.

Check the render method of %s.`, dt(En) || "Unknown"));
      var v = Oo(s, f);
      v.payload = {
        element: e
      }, i = i === void 0 ? null : i, i !== null && (typeof i != "function" && y("render(...): Expected the last optional `callback` argument to be a function. Instead received: %s.", i), v.callback = i);
      var g = Vu(o, v, f);
      return g !== null && (xr(g, o, f, s), dm(g, o, f)), f;
    }
    function ty(e) {
      var t = e.current;
      if (!t.child)
        return null;
      switch (t.child.tag) {
        case V:
          return t.child.stateNode;
        default:
          return t.child.stateNode;
      }
    }
    function y_(e) {
      switch (e.tag) {
        case ne: {
          var t = e.stateNode;
          if (af(t)) {
            var a = Bd(t);
            kk(t, a);
          }
          break;
        }
        case ke: {
          zo(function() {
            var o = Ja(e, Qe);
            if (o !== null) {
              var s = Na();
              xr(o, e, Qe, s);
            }
          });
          var i = Qe;
          DS(e, i);
          break;
        }
      }
    }
    function ZC(e, t) {
      var a = e.memoizedState;
      a !== null && a.dehydrated !== null && (a.retryLane = sh(a.retryLane, t));
    }
    function DS(e, t) {
      ZC(e, t);
      var a = e.alternate;
      a && ZC(a, t);
    }
    function g_(e) {
      if (e.tag === ke) {
        var t = Rs, a = Ja(e, t);
        if (a !== null) {
          var i = Na();
          xr(a, e, t, i);
        }
        DS(e, t);
      }
    }
    function S_(e) {
      if (e.tag === ke) {
        var t = qu(e), a = Ja(e, t);
        if (a !== null) {
          var i = Na();
          xr(a, e, t, i);
        }
        DS(e, t);
      }
    }
    function eE(e) {
      var t = Yv(e);
      return t === null ? null : t.stateNode;
    }
    var tE = function(e) {
      return null;
    };
    function x_(e) {
      return tE(e);
    }
    var nE = function(e) {
      return !1;
    };
    function b_(e) {
      return nE(e);
    }
    var rE = null, aE = null, iE = null, lE = null, oE = null, uE = null, sE = null, cE = null, fE = null;
    {
      var dE = function(e, t, a) {
        var i = t[a], o = At(e) ? e.slice() : Et({}, e);
        return a + 1 === t.length ? (At(o) ? o.splice(i, 1) : delete o[i], o) : (o[i] = dE(e[i], t, a + 1), o);
      }, pE = function(e, t) {
        return dE(e, t, 0);
      }, vE = function(e, t, a, i) {
        var o = t[i], s = At(e) ? e.slice() : Et({}, e);
        if (i + 1 === t.length) {
          var f = a[i];
          s[f] = s[o], At(s) ? s.splice(o, 1) : delete s[o];
        } else
          s[o] = vE(
            // $FlowFixMe number or string is fine here
            e[o],
            t,
            a,
            i + 1
          );
        return s;
      }, hE = function(e, t, a) {
        if (t.length !== a.length) {
          W("copyWithRename() expects paths of the same length");
          return;
        } else
          for (var i = 0; i < a.length - 1; i++)
            if (t[i] !== a[i]) {
              W("copyWithRename() expects paths to be the same except for the deepest key");
              return;
            }
        return vE(e, t, a, 0);
      }, mE = function(e, t, a, i) {
        if (a >= t.length)
          return i;
        var o = t[a], s = At(e) ? e.slice() : Et({}, e);
        return s[o] = mE(e[o], t, a + 1, i), s;
      }, yE = function(e, t, a) {
        return mE(e, t, 0, a);
      }, NS = function(e, t) {
        for (var a = e.memoizedState; a !== null && t > 0; )
          a = a.next, t--;
        return a;
      };
      rE = function(e, t, a, i) {
        var o = NS(e, t);
        if (o !== null) {
          var s = yE(o.memoizedState, a, i);
          o.memoizedState = s, o.baseState = s, e.memoizedProps = Et({}, e.memoizedProps);
          var f = Ja(e, Qe);
          f !== null && xr(f, e, Qe, fn);
        }
      }, aE = function(e, t, a) {
        var i = NS(e, t);
        if (i !== null) {
          var o = pE(i.memoizedState, a);
          i.memoizedState = o, i.baseState = o, e.memoizedProps = Et({}, e.memoizedProps);
          var s = Ja(e, Qe);
          s !== null && xr(s, e, Qe, fn);
        }
      }, iE = function(e, t, a, i) {
        var o = NS(e, t);
        if (o !== null) {
          var s = hE(o.memoizedState, a, i);
          o.memoizedState = s, o.baseState = s, e.memoizedProps = Et({}, e.memoizedProps);
          var f = Ja(e, Qe);
          f !== null && xr(f, e, Qe, fn);
        }
      }, lE = function(e, t, a) {
        e.pendingProps = yE(e.memoizedProps, t, a), e.alternate && (e.alternate.pendingProps = e.pendingProps);
        var i = Ja(e, Qe);
        i !== null && xr(i, e, Qe, fn);
      }, oE = function(e, t) {
        e.pendingProps = pE(e.memoizedProps, t), e.alternate && (e.alternate.pendingProps = e.pendingProps);
        var a = Ja(e, Qe);
        a !== null && xr(a, e, Qe, fn);
      }, uE = function(e, t, a) {
        e.pendingProps = hE(e.memoizedProps, t, a), e.alternate && (e.alternate.pendingProps = e.pendingProps);
        var i = Ja(e, Qe);
        i !== null && xr(i, e, Qe, fn);
      }, sE = function(e) {
        var t = Ja(e, Qe);
        t !== null && xr(t, e, Qe, fn);
      }, cE = function(e) {
        tE = e;
      }, fE = function(e) {
        nE = e;
      };
    }
    function C_(e) {
      var t = Ba(e);
      return t === null ? null : t.stateNode;
    }
    function E_(e) {
      return null;
    }
    function w_() {
      return En;
    }
    function R_(e) {
      var t = e.findFiberByHostInstance, a = b.ReactCurrentDispatcher;
      return zd({
        bundleType: e.bundleType,
        version: e.version,
        rendererPackageName: e.rendererPackageName,
        rendererConfig: e.rendererConfig,
        overrideHookState: rE,
        overrideHookStateDeletePath: aE,
        overrideHookStateRenamePath: iE,
        overrideProps: lE,
        overridePropsDeletePath: oE,
        overridePropsRenamePath: uE,
        setErrorHandler: cE,
        setSuspenseHandler: fE,
        scheduleUpdate: sE,
        currentDispatcherRef: a,
        findHostInstanceByFiber: C_,
        findFiberByHostInstance: t || E_,
        // React Refresh
        findHostInstancesForRefresh: t_,
        scheduleRefresh: Zk,
        scheduleRoot: e_,
        setRefreshHandler: Jk,
        // Enables DevTools to append owner stacks to error messages in DEV mode.
        getCurrentFiber: w_,
        // Enables DevTools to detect reconciler version rather than renderer version
        // which may not match for third party renderers.
        reconcilerVersion: TS
      });
    }
    var gE = typeof reportError == "function" ? (
      // In modern browsers, reportError will dispatch an error event,
      // emulating an uncaught JavaScript error.
      reportError
    ) : function(e) {
      console.error(e);
    };
    function OS(e) {
      this._internalRoot = e;
    }
    ny.prototype.render = OS.prototype.render = function(e) {
      var t = this._internalRoot;
      if (t === null)
        throw new Error("Cannot update an unmounted root.");
      {
        typeof arguments[1] == "function" ? y("render(...): does not support the second callback argument. To execute a side effect after rendering, declare it in a component body with useEffect().") : ry(arguments[1]) ? y("You passed a container to the second argument of root.render(...). You don't need to pass it again since you already passed it to create the root.") : typeof arguments[1] < "u" && y("You passed a second argument to root.render(...) but it only accepts one argument.");
        var a = t.containerInfo;
        if (a.nodeType !== Vn) {
          var i = eE(t.current);
          i && i.parentNode !== a && y("render(...): It looks like the React-rendered content of the root container was removed without using React. This is not supported and will cause errors. Instead, call root.unmount() to empty a root's container.");
        }
      }
      iv(e, t, null, null);
    }, ny.prototype.unmount = OS.prototype.unmount = function() {
      typeof arguments[0] == "function" && y("unmount(...): does not support a callback argument. To execute a side effect after rendering, declare it in a component body with useEffect().");
      var e = this._internalRoot;
      if (e !== null) {
        this._internalRoot = null;
        var t = e.containerInfo;
        NC() && y("Attempted to synchronously unmount a root while React was already rendering. React cannot finish unmounting the root until the current render has completed, which may lead to a race condition."), zo(function() {
          iv(null, e, null, null);
        }), gx(t);
      }
    };
    function T_(e, t) {
      if (!ry(e))
        throw new Error("createRoot(...): Target container is not a DOM element.");
      SE(e);
      var a = !1, i = !1, o = "", s = gE;
      t != null && (t.hydrate ? W("hydrate through createRoot is deprecated. Use ReactDOMClient.hydrateRoot(container, <App />) instead.") : typeof t == "object" && t !== null && t.$$typeof === ii && y(`You passed a JSX element to createRoot. You probably meant to call root.render instead. Example usage:

  let root = createRoot(domContainer);
  root.render(<App />);`), t.unstable_strictMode === !0 && (a = !0), t.identifierPrefix !== void 0 && (o = t.identifierPrefix), t.onRecoverableError !== void 0 && (s = t.onRecoverableError), t.transitionCallbacks !== void 0 && t.transitionCallbacks);
      var f = KC(e, Kh, null, a, i, o, s);
      Ih(f.current, e);
      var p = e.nodeType === Vn ? e.parentNode : e;
      return fp(p), new OS(f);
    }
    function ny(e) {
      this._internalRoot = e;
    }
    function k_(e) {
      e && Ly(e);
    }
    ny.prototype.unstable_scheduleHydration = k_;
    function __(e, t, a) {
      if (!ry(e))
        throw new Error("hydrateRoot(...): Target container is not a DOM element.");
      SE(e), t === void 0 && y("Must provide initial children as second argument to hydrateRoot. Example usage: hydrateRoot(domContainer, <App />)");
      var i = a ?? null, o = a != null && a.hydratedSources || null, s = !1, f = !1, p = "", v = gE;
      a != null && (a.unstable_strictMode === !0 && (s = !0), a.identifierPrefix !== void 0 && (p = a.identifierPrefix), a.onRecoverableError !== void 0 && (v = a.onRecoverableError));
      var g = JC(t, null, e, Kh, i, s, f, p, v);
      if (Ih(g.current, e), fp(e), o)
        for (var x = 0; x < o.length; x++) {
          var N = o[x];
          MR(g, N);
        }
      return new ny(g);
    }
    function ry(e) {
      return !!(e && (e.nodeType === ta || e.nodeType === si || e.nodeType === to || !q));
    }
    function lv(e) {
      return !!(e && (e.nodeType === ta || e.nodeType === si || e.nodeType === to || e.nodeType === Vn && e.nodeValue === " react-mount-point-unstable "));
    }
    function SE(e) {
      e.nodeType === ta && e.tagName && e.tagName.toUpperCase() === "BODY" && y("createRoot(): Creating roots directly with document.body is discouraged, since its children are often manipulated by third-party scripts and browser extensions. This may lead to subtle reconciliation issues. Try using a container element created for your app."), Cp(e) && (e._reactRootContainer ? y("You are calling ReactDOMClient.createRoot() on a container that was previously passed to ReactDOM.render(). This is not supported.") : y("You are calling ReactDOMClient.createRoot() on a container that has already been passed to createRoot() before. Instead, call root.render() on the existing root instead if you want to update it."));
    }
    var D_ = b.ReactCurrentOwner, xE;
    xE = function(e) {
      if (e._reactRootContainer && e.nodeType !== Vn) {
        var t = eE(e._reactRootContainer.current);
        t && t.parentNode !== e && y("render(...): It looks like the React-rendered content of this container was removed without using React. This is not supported and will cause errors. Instead, call ReactDOM.unmountComponentAtNode to empty a container.");
      }
      var a = !!e._reactRootContainer, i = MS(e), o = !!(i && Au(i));
      o && !a && y("render(...): Replacing React-rendered children with a new root component. If you intended to update the children of this node, you should instead have the existing children update their state and render the new components instead of calling ReactDOM.render."), e.nodeType === ta && e.tagName && e.tagName.toUpperCase() === "BODY" && y("render(): Rendering components directly into document.body is discouraged, since its children are often manipulated by third-party scripts and browser extensions. This may lead to subtle reconciliation issues. Try rendering into a container element created for your app.");
    };
    function MS(e) {
      return e ? e.nodeType === si ? e.documentElement : e.firstChild : null;
    }
    function bE() {
    }
    function N_(e, t, a, i, o) {
      if (o) {
        if (typeof i == "function") {
          var s = i;
          i = function() {
            var _ = ty(f);
            s.call(_);
          };
        }
        var f = JC(
          t,
          i,
          e,
          Fu,
          null,
          // hydrationCallbacks
          !1,
          // isStrictMode
          !1,
          // concurrentUpdatesByDefaultOverride,
          "",
          // identifierPrefix
          bE
        );
        e._reactRootContainer = f, Ih(f.current, e);
        var p = e.nodeType === Vn ? e.parentNode : e;
        return fp(p), zo(), f;
      } else {
        for (var v; v = e.lastChild; )
          e.removeChild(v);
        if (typeof i == "function") {
          var g = i;
          i = function() {
            var _ = ty(x);
            g.call(_);
          };
        }
        var x = KC(
          e,
          Fu,
          null,
          // hydrationCallbacks
          !1,
          // isStrictMode
          !1,
          // concurrentUpdatesByDefaultOverride,
          "",
          // identifierPrefix
          bE
        );
        e._reactRootContainer = x, Ih(x.current, e);
        var N = e.nodeType === Vn ? e.parentNode : e;
        return fp(N), zo(function() {
          iv(t, x, a, i);
        }), x;
      }
    }
    function O_(e, t) {
      e !== null && typeof e != "function" && y("%s(...): Expected the last optional `callback` argument to be a function. Instead received: %s.", t, e);
    }
    function ay(e, t, a, i, o) {
      xE(a), O_(o === void 0 ? null : o, "render");
      var s = a._reactRootContainer, f;
      if (!s)
        f = N_(a, t, e, o, i);
      else {
        if (f = s, typeof o == "function") {
          var p = o;
          o = function() {
            var v = ty(f);
            p.call(v);
          };
        }
        iv(t, f, e, o);
      }
      return ty(f);
    }
    var CE = !1;
    function M_(e) {
      {
        CE || (CE = !0, y("findDOMNode is deprecated and will be removed in the next major release. Instead, add a ref directly to the element you want to reference. Learn more about using refs safely here: https://reactjs.org/link/strict-mode-find-node"));
        var t = D_.current;
        if (t !== null && t.stateNode !== null) {
          var a = t.stateNode._warnedAboutRefsInRender;
          a || y("%s is accessing findDOMNode inside its render(). render() should be a pure function of props and state. It should never access something that requires stale data from the previous render, such as refs. Move this logic to componentDidMount and componentDidUpdate instead.", zt(t.type) || "A component"), t.stateNode._warnedAboutRefsInRender = !0;
        }
      }
      return e == null ? null : e.nodeType === ta ? e : m_(e, "findDOMNode");
    }
    function L_(e, t, a) {
      if (y("ReactDOM.hydrate is no longer supported in React 18. Use hydrateRoot instead. Until you switch to the new API, your app will behave as if it's running React 17. Learn more: https://reactjs.org/link/switch-to-createroot"), !lv(t))
        throw new Error("Target container is not a DOM element.");
      {
        var i = Cp(t) && t._reactRootContainer === void 0;
        i && y("You are calling ReactDOM.hydrate() on a container that was previously passed to ReactDOMClient.createRoot(). This is not supported. Did you mean to call hydrateRoot(container, element)?");
      }
      return ay(null, e, t, !0, a);
    }
    function j_(e, t, a) {
      if (y("ReactDOM.render is no longer supported in React 18. Use createRoot instead. Until you switch to the new API, your app will behave as if it's running React 17. Learn more: https://reactjs.org/link/switch-to-createroot"), !lv(t))
        throw new Error("Target container is not a DOM element.");
      {
        var i = Cp(t) && t._reactRootContainer === void 0;
        i && y("You are calling ReactDOM.render() on a container that was previously passed to ReactDOMClient.createRoot(). This is not supported. Did you mean to call root.render(element)?");
      }
      return ay(null, e, t, !1, a);
    }
    function z_(e, t, a, i) {
      if (y("ReactDOM.unstable_renderSubtreeIntoContainer() is no longer supported in React 18. Consider using a portal instead. Until you switch to the createRoot API, your app will behave as if it's running React 17. Learn more: https://reactjs.org/link/switch-to-createroot"), !lv(a))
        throw new Error("Target container is not a DOM element.");
      if (e == null || !ms(e))
        throw new Error("parentComponent must be a valid React Component");
      return ay(e, t, a, !1, i);
    }
    var EE = !1;
    function A_(e) {
      if (EE || (EE = !0, y("unmountComponentAtNode is deprecated and will be removed in the next major release. Switch to the createRoot API. Learn more: https://reactjs.org/link/switch-to-createroot")), !lv(e))
        throw new Error("unmountComponentAtNode(...): Target container is not a DOM element.");
      {
        var t = Cp(e) && e._reactRootContainer === void 0;
        t && y("You are calling ReactDOM.unmountComponentAtNode() on a container that was previously passed to ReactDOMClient.createRoot(). This is not supported. Did you mean to call root.unmount()?");
      }
      if (e._reactRootContainer) {
        {
          var a = MS(e), i = a && !Au(a);
          i && y("unmountComponentAtNode(): The node you're attempting to unmount was rendered by another copy of React.");
        }
        return zo(function() {
          ay(null, null, e, !1, function() {
            e._reactRootContainer = null, gx(e);
          });
        }), !0;
      } else {
        {
          var o = MS(e), s = !!(o && Au(o)), f = e.nodeType === ta && lv(e.parentNode) && !!e.parentNode._reactRootContainer;
          s && y("unmountComponentAtNode(): The node you're attempting to unmount was rendered by React and is not a top-level container. %s", f ? "You may have accidentally passed in a React root node instead of its container." : "Instead, have the parent component update its state and rerender in order to remove this component.");
        }
        return !1;
      }
    }
    Cu(y_), Oy(g_), of(S_), dh(Wa), ph(Dr), (typeof Map != "function" || // $FlowIssue Flow incorrectly thinks Map has no prototype
    Map.prototype == null || typeof Map.prototype.forEach != "function" || typeof Set != "function" || // $FlowIssue Flow incorrectly thinks Set has no prototype
    Set.prototype == null || typeof Set.prototype.clear != "function" || typeof Set.prototype.forEach != "function") && y("React depends on Map and Set built-in types. Make sure that you load a polyfill in older browsers. https://reactjs.org/link/react-polyfills"), Bv(F1), Ec(sS, _k, zo);
    function U_(e, t) {
      var a = arguments.length > 2 && arguments[2] !== void 0 ? arguments[2] : null;
      if (!ry(t))
        throw new Error("Target container is not a DOM element.");
      return h_(e, t, null, a);
    }
    function F_(e, t, a, i) {
      return z_(e, t, a, i);
    }
    var LS = {
      usingClientEntryPoint: !1,
      // Keep in sync with ReactTestUtils.js.
      // This is an array for better minification.
      Events: [Au, Nf, Yh, Cc, ps, sS]
    };
    function H_(e, t) {
      return LS.usingClientEntryPoint || y('You are importing createRoot from "react-dom" which is not supported. You should instead import it from "react-dom/client".'), T_(e, t);
    }
    function P_(e, t, a) {
      return LS.usingClientEntryPoint || y('You are importing hydrateRoot from "react-dom" which is not supported. You should instead import it from "react-dom/client".'), __(e, t, a);
    }
    function V_(e) {
      return NC() && y("flushSync was called from inside a lifecycle method. React cannot flush when React is already rendering. Consider moving this call to a scheduler task or micro task."), zo(e);
    }
    var B_ = R_({
      findFiberByHostInstance: $s,
      bundleType: 1,
      version: TS,
      rendererPackageName: "react-dom"
    });
    if (!B_ && xn && window.top === window.self && (navigator.userAgent.indexOf("Chrome") > -1 && navigator.userAgent.indexOf("Edge") === -1 || navigator.userAgent.indexOf("Firefox") > -1)) {
      var wE = window.location.protocol;
      /^(https?|file):$/.test(wE) && console.info("%cDownload the React DevTools for a better development experience: https://reactjs.org/link/react-devtools" + (wE === "file:" ? `
You might need to use a local HTTP server (instead of file://): https://reactjs.org/link/react-devtools-faq` : ""), "font-weight:bold");
    }
    ri.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED = LS, ri.createPortal = U_, ri.createRoot = H_, ri.findDOMNode = M_, ri.flushSync = V_, ri.hydrate = L_, ri.hydrateRoot = P_, ri.render = j_, ri.unmountComponentAtNode = A_, ri.unstable_batchedUpdates = sS, ri.unstable_renderSubtreeIntoContainer = F_, ri.version = TS, typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ < "u" && typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.registerInternalModuleStop == "function" && __REACT_DEVTOOLS_GLOBAL_HOOK__.registerInternalModuleStop(new Error());
  }()), ri;
}
function VE() {
  if (!(typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ > "u" || typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE != "function")) {
    if (process.env.NODE_ENV !== "production")
      throw new Error("^_^");
    try {
      __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE(VE);
    } catch (S) {
      console.error(S);
    }
  }
}
process.env.NODE_ENV === "production" ? (VE(), PS.exports = Z_()) : PS.exports = eD();
var tD = PS.exports, cv = tD;
if (process.env.NODE_ENV === "production")
  hv.createRoot = cv.createRoot, hv.hydrateRoot = cv.hydrateRoot;
else {
  var ly = cv.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED;
  hv.createRoot = function(S, w) {
    ly.usingClientEntryPoint = !0;
    try {
      return cv.createRoot(S, w);
    } finally {
      ly.usingClientEntryPoint = !1;
    }
  }, hv.hydrateRoot = function(S, w, b) {
    ly.usingClientEntryPoint = !0;
    try {
      return cv.hydrateRoot(S, w, b);
    } finally {
      ly.usingClientEntryPoint = !1;
    }
  };
}
class fv {
  constructor(w) {
    this.vscode = w;
  }
  /**
   * Send message to VS Code extension
   */
  postMessage(w) {
    this.vscode ? (console.log("[VSCodeBridge] Sending message:", w), this.vscode.postMessage(w)) : console.warn("[VSCodeBridge] VS Code API not available");
  }
  /**
   * Request data from extension
   */
  requestData(w, b) {
    this.postMessage({
      type: "request-data",
      requestType: w,
      params: b
    });
  }
  /**
   * Send HITL response
   */
  sendHITLResponse(w, b, U) {
    this.postMessage({
      type: "hitl_response",
      request_id: w,
      decision: b,
      data: U
    });
  }
  /**
   * Request session details
   */
  requestSessionDetails(w) {
    this.requestData("session-details", { sessionId: w });
  }
  /**
   * Request sessions list
   */
  requestSessionsList(w) {
    this.requestData("sessions-list", w);
  }
  /**
   * Send research command
   */
  startResearch(w) {
    this.postMessage({
      type: "start-research",
      topic: w
    });
  }
  /**
   * Update session filter
   */
  updateFilter(w, b) {
    this.postMessage({
      type: "update-filter",
      filterType: w,
      value: b
    });
  }
  /**
   * Export manuscript
   */
  exportManuscript(w, b) {
    this.postMessage({
      type: "export-manuscript",
      sessionId: w,
      format: b
    });
  }
  /**
   * Open paper
   */
  openPaper(w, b) {
    this.postMessage({
      type: "open-paper",
      sessionId: w,
      paperId: b
    });
  }
}
function BE(S) {
  var w, b, U = "";
  if (typeof S == "string" || typeof S == "number")
    U += S;
  else if (typeof S == "object")
    if (Array.isArray(S)) {
      var X = S.length;
      for (w = 0; w < X; w++)
        S[w] && (b = BE(S[w])) && (U && (U += " "), U += b);
    } else
      for (b in S)
        S[b] && (U && (U += " "), U += b);
  return U;
}
function nD() {
  for (var S, w, b = 0, U = "", X = arguments.length; b < X; b++)
    (S = arguments[b]) && (w = BE(S)) && (U && (U += " "), U += w);
  return U;
}
const rD = (S, w) => {
  const b = new Array(S.length + w.length);
  for (let U = 0; U < S.length; U++)
    b[U] = S[U];
  for (let U = 0; U < w.length; U++)
    b[S.length + U] = w[U];
  return b;
}, aD = (S, w) => ({
  classGroupId: S,
  validator: w
}), $E = (S = /* @__PURE__ */ new Map(), w = null, b) => ({
  nextPart: S,
  validators: w,
  classGroupId: b
}), cy = "-", jE = [], iD = "arbitrary..", lD = (S) => {
  const w = uD(S), {
    conflictingClassGroups: b,
    conflictingClassGroupModifiers: U
  } = S;
  return {
    getClassGroupId: (y) => {
      if (y.startsWith("[") && y.endsWith("]"))
        return oD(y);
      const ce = y.split(cy), B = ce[0] === "" && ce.length > 1 ? 1 : 0;
      return IE(ce, B, w);
    },
    getConflictingClassGroupIds: (y, ce) => {
      if (ce) {
        const B = U[y], K = b[y];
        return B ? K ? rD(K, B) : B : K || jE;
      }
      return b[y] || jE;
    }
  };
}, IE = (S, w, b) => {
  if (S.length - w === 0)
    return b.classGroupId;
  const X = S[w], W = b.nextPart.get(X);
  if (W) {
    const K = IE(S, w + 1, W);
    if (K)
      return K;
  }
  const y = b.validators;
  if (y === null)
    return;
  const ce = w === 0 ? S.join(cy) : S.slice(w).join(cy), B = y.length;
  for (let K = 0; K < B; K++) {
    const ye = y[K];
    if (ye.validator(ce))
      return ye.classGroupId;
  }
}, oD = (S) => S.slice(1, -1).indexOf(":") === -1 ? void 0 : (() => {
  const w = S.slice(1, -1), b = w.indexOf(":"), U = w.slice(0, b);
  return U ? iD + U : void 0;
})(), uD = (S) => {
  const {
    theme: w,
    classGroups: b
  } = S;
  return sD(b, w);
}, sD = (S, w) => {
  const b = $E();
  for (const U in S) {
    const X = S[U];
    BS(X, b, U, w);
  }
  return b;
}, BS = (S, w, b, U) => {
  const X = S.length;
  for (let W = 0; W < X; W++) {
    const y = S[W];
    cD(y, w, b, U);
  }
}, cD = (S, w, b, U) => {
  if (typeof S == "string") {
    fD(S, w, b);
    return;
  }
  if (typeof S == "function") {
    dD(S, w, b, U);
    return;
  }
  pD(S, w, b, U);
}, fD = (S, w, b) => {
  const U = S === "" ? w : YE(w, S);
  U.classGroupId = b;
}, dD = (S, w, b, U) => {
  if (vD(S)) {
    BS(S(U), w, b, U);
    return;
  }
  w.validators === null && (w.validators = []), w.validators.push(aD(b, S));
}, pD = (S, w, b, U) => {
  const X = Object.entries(S), W = X.length;
  for (let y = 0; y < W; y++) {
    const [ce, B] = X[y];
    BS(B, YE(w, ce), b, U);
  }
}, YE = (S, w) => {
  let b = S;
  const U = w.split(cy), X = U.length;
  for (let W = 0; W < X; W++) {
    const y = U[W];
    let ce = b.nextPart.get(y);
    ce || (ce = $E(), b.nextPart.set(y, ce)), b = ce;
  }
  return b;
}, vD = (S) => "isThemeGetter" in S && S.isThemeGetter === !0, hD = (S) => {
  if (S < 1)
    return {
      get: () => {
      },
      set: () => {
      }
    };
  let w = 0, b = /* @__PURE__ */ Object.create(null), U = /* @__PURE__ */ Object.create(null);
  const X = (W, y) => {
    b[W] = y, w++, w > S && (w = 0, U = b, b = /* @__PURE__ */ Object.create(null));
  };
  return {
    get(W) {
      let y = b[W];
      if (y !== void 0)
        return y;
      if ((y = U[W]) !== void 0)
        return X(W, y), y;
    },
    set(W, y) {
      W in b ? b[W] = y : X(W, y);
    }
  };
}, VS = "!", zE = ":", mD = [], AE = (S, w, b, U, X) => ({
  modifiers: S,
  hasImportantModifier: w,
  baseClassName: b,
  maybePostfixModifierPosition: U,
  isExternal: X
}), yD = (S) => {
  const {
    prefix: w,
    experimentalParseClassName: b
  } = S;
  let U = (X) => {
    const W = [];
    let y = 0, ce = 0, B = 0, K;
    const ye = X.length;
    for (let de = 0; de < ye; de++) {
      const Ae = X[de];
      if (y === 0 && ce === 0) {
        if (Ae === zE) {
          W.push(X.slice(B, de)), B = de + 1;
          continue;
        }
        if (Ae === "/") {
          K = de;
          continue;
        }
      }
      Ae === "[" ? y++ : Ae === "]" ? y-- : Ae === "(" ? ce++ : Ae === ")" && ce--;
    }
    const ne = W.length === 0 ? X : X.slice(B);
    let oe = ne, V = !1;
    ne.endsWith(VS) ? (oe = ne.slice(0, -1), V = !0) : (
      /**
       * In Tailwind CSS v3 the important modifier was at the start of the base class name. This is still supported for legacy reasons.
       * @see https://github.com/dcastil/tailwind-merge/issues/513#issuecomment-2614029864
       */
      ne.startsWith(VS) && (oe = ne.slice(1), V = !0)
    );
    const $ = K && K > B ? K - B : void 0;
    return AE(W, V, oe, $);
  };
  if (w) {
    const X = w + zE, W = U;
    U = (y) => y.startsWith(X) ? W(y.slice(X.length)) : AE(mD, !1, y, void 0, !0);
  }
  if (b) {
    const X = U;
    U = (W) => b({
      className: W,
      parseClassName: X
    });
  }
  return U;
}, gD = (S) => {
  const w = /* @__PURE__ */ new Map();
  return S.orderSensitiveModifiers.forEach((b, U) => {
    w.set(b, 1e6 + U);
  }), (b) => {
    const U = [];
    let X = [];
    for (let W = 0; W < b.length; W++) {
      const y = b[W], ce = y[0] === "[", B = w.has(y);
      ce || B ? (X.length > 0 && (X.sort(), U.push(...X), X = []), U.push(y)) : X.push(y);
    }
    return X.length > 0 && (X.sort(), U.push(...X)), U;
  };
}, SD = (S) => ({
  cache: hD(S.cacheSize),
  parseClassName: yD(S),
  sortModifiers: gD(S),
  ...lD(S)
}), xD = /\s+/, bD = (S, w) => {
  const {
    parseClassName: b,
    getClassGroupId: U,
    getConflictingClassGroupIds: X,
    sortModifiers: W
  } = w, y = [], ce = S.trim().split(xD);
  let B = "";
  for (let K = ce.length - 1; K >= 0; K -= 1) {
    const ye = ce[K], {
      isExternal: ne,
      modifiers: oe,
      hasImportantModifier: V,
      baseClassName: $,
      maybePostfixModifierPosition: de
    } = b(ye);
    if (ne) {
      B = ye + (B.length > 0 ? " " + B : B);
      continue;
    }
    let Ae = !!de, Dt = U(Ae ? $.substring(0, de) : $);
    if (!Dt) {
      if (!Ae) {
        B = ye + (B.length > 0 ? " " + B : B);
        continue;
      }
      if (Dt = U($), !Dt) {
        B = ye + (B.length > 0 ? " " + B : B);
        continue;
      }
      Ae = !1;
    }
    const rt = oe.length === 0 ? "" : oe.length === 1 ? oe[0] : W(oe).join(":"), Ke = V ? rt + VS : rt, ct = Ke + Dt;
    if (y.indexOf(ct) > -1)
      continue;
    y.push(ct);
    const ke = X(Dt, Ae);
    for (let at = 0; at < ke.length; ++at) {
      const Ye = ke[at];
      y.push(Ke + Ye);
    }
    B = ye + (B.length > 0 ? " " + B : B);
  }
  return B;
}, CD = (...S) => {
  let w = 0, b, U, X = "";
  for (; w < S.length; )
    (b = S[w++]) && (U = WE(b)) && (X && (X += " "), X += U);
  return X;
}, WE = (S) => {
  if (typeof S == "string")
    return S;
  let w, b = "";
  for (let U = 0; U < S.length; U++)
    S[U] && (w = WE(S[U])) && (b && (b += " "), b += w);
  return b;
}, ED = (S, ...w) => {
  let b, U, X, W;
  const y = (B) => {
    const K = w.reduce((ye, ne) => ne(ye), S());
    return b = SD(K), U = b.cache.get, X = b.cache.set, W = ce, ce(B);
  }, ce = (B) => {
    const K = U(B);
    if (K)
      return K;
    const ye = bD(B, b);
    return X(B, ye), ye;
  };
  return W = y, (...B) => W(CD(...B));
}, wD = [], br = (S) => {
  const w = (b) => b[S] || wD;
  return w.isThemeGetter = !0, w;
}, QE = /^\[(?:(\w[\w-]*):)?(.+)\]$/i, GE = /^\((?:(\w[\w-]*):)?(.+)\)$/i, RD = /^\d+\/\d+$/, TD = /^(\d+(\.\d+)?)?(xs|sm|md|lg|xl)$/, kD = /\d+(%|px|r?em|[sdl]?v([hwib]|min|max)|pt|pc|in|cm|mm|cap|ch|ex|r?lh|cq(w|h|i|b|min|max))|\b(calc|min|max|clamp)\(.+\)|^0$/, _D = /^(rgba?|hsla?|hwb|(ok)?(lab|lch)|color-mix)\(.+\)$/, DD = /^(inset_)?-?((\d+)?\.?(\d+)[a-z]+|0)_-?((\d+)?\.?(\d+)[a-z]+|0)/, ND = /^(url|image|image-set|cross-fade|element|(repeating-)?(linear|radial|conic)-gradient)\(.+\)$/, td = (S) => RD.test(S), Lt = (S) => !!S && !Number.isNaN(Number(S)), Ju = (S) => !!S && Number.isInteger(Number(S)), AS = (S) => S.endsWith("%") && Lt(S.slice(0, -1)), Fo = (S) => TD.test(S), OD = () => !0, MD = (S) => (
  // `colorFunctionRegex` check is necessary because color functions can have percentages in them which which would be incorrectly classified as lengths.
  // For example, `hsl(0 0% 0%)` would be classified as a length without this check.
  // I could also use lookbehind assertion in `lengthUnitRegex` but that isn't supported widely enough.
  kD.test(S) && !_D.test(S)
), qE = () => !1, LD = (S) => DD.test(S), jD = (S) => ND.test(S), zD = (S) => !je(S) && !ze(S), AD = (S) => rd(S, JE, qE), je = (S) => QE.test(S), ic = (S) => rd(S, ZE, MD), US = (S) => rd(S, VD, Lt), UE = (S) => rd(S, XE, qE), UD = (S) => rd(S, KE, jD), oy = (S) => rd(S, e1, LD), ze = (S) => GE.test(S), dv = (S) => ad(S, ZE), FD = (S) => ad(S, BD), FE = (S) => ad(S, XE), HD = (S) => ad(S, JE), PD = (S) => ad(S, KE), uy = (S) => ad(S, e1, !0), rd = (S, w, b) => {
  const U = QE.exec(S);
  return U ? U[1] ? w(U[1]) : b(U[2]) : !1;
}, ad = (S, w, b = !1) => {
  const U = GE.exec(S);
  return U ? U[1] ? w(U[1]) : b : !1;
}, XE = (S) => S === "position" || S === "percentage", KE = (S) => S === "image" || S === "url", JE = (S) => S === "length" || S === "size" || S === "bg-size", ZE = (S) => S === "length", VD = (S) => S === "number", BD = (S) => S === "family-name", e1 = (S) => S === "shadow", $D = () => {
  const S = br("color"), w = br("font"), b = br("text"), U = br("font-weight"), X = br("tracking"), W = br("leading"), y = br("breakpoint"), ce = br("container"), B = br("spacing"), K = br("radius"), ye = br("shadow"), ne = br("inset-shadow"), oe = br("text-shadow"), V = br("drop-shadow"), $ = br("blur"), de = br("perspective"), Ae = br("aspect"), Dt = br("ease"), rt = br("animate"), Ke = () => ["auto", "avoid", "all", "avoid-page", "page", "left", "right", "column"], ct = () => [
    "center",
    "top",
    "bottom",
    "left",
    "right",
    "top-left",
    // Deprecated since Tailwind CSS v4.1.0, see https://github.com/tailwindlabs/tailwindcss/pull/17378
    "left-top",
    "top-right",
    // Deprecated since Tailwind CSS v4.1.0, see https://github.com/tailwindlabs/tailwindcss/pull/17378
    "right-top",
    "bottom-right",
    // Deprecated since Tailwind CSS v4.1.0, see https://github.com/tailwindlabs/tailwindcss/pull/17378
    "right-bottom",
    "bottom-left",
    // Deprecated since Tailwind CSS v4.1.0, see https://github.com/tailwindlabs/tailwindcss/pull/17378
    "left-bottom"
  ], ke = () => [...ct(), ze, je], at = () => ["auto", "hidden", "clip", "visible", "scroll"], Ye = () => ["auto", "contain", "none"], be = () => [ze, je, B], Oe = () => [td, "full", "auto", ...be()], $e = () => [Ju, "none", "subgrid", ze, je], it = () => ["auto", {
    span: ["full", Ju, ze, je]
  }, Ju, ze, je], Rt = () => [Ju, "auto", ze, je], Ie = () => ["auto", "min", "max", "fr", ze, je], st = () => ["start", "end", "center", "between", "around", "evenly", "stretch", "baseline", "center-safe", "end-safe"], Nt = () => ["start", "end", "center", "stretch", "center-safe", "end-safe"], yt = () => ["auto", ...be()], Se = () => [td, "auto", "full", "dvw", "dvh", "lvw", "lvh", "svw", "svh", "min", "max", "fit", ...be()], I = () => [S, ze, je], Ue = () => [...ct(), FE, UE, {
    position: [ze, je]
  }], pe = () => ["no-repeat", {
    repeat: ["", "x", "y", "space", "round"]
  }], O = () => ["auto", "cover", "contain", HD, AD, {
    size: [ze, je]
  }], q = () => [AS, dv, ic], Re = () => [
    // Deprecated since Tailwind CSS v4.0.0
    "",
    "none",
    "full",
    K,
    ze,
    je
  ], Me = () => ["", Lt, dv, ic], ft = () => ["solid", "dashed", "dotted", "double"], vt = () => ["normal", "multiply", "screen", "overlay", "darken", "lighten", "color-dodge", "color-burn", "hard-light", "soft-light", "difference", "exclusion", "hue", "saturation", "color", "luminosity"], Ge = () => [Lt, AS, FE, UE], St = () => [
    // Deprecated since Tailwind CSS v4.0.0
    "",
    "none",
    $,
    ze,
    je
  ], ht = () => ["none", Lt, ze, je], Wt = () => ["none", Lt, ze, je], Fn = () => [Lt, ze, je], Yn = () => [td, "full", ...be()];
  return {
    cacheSize: 500,
    theme: {
      animate: ["spin", "ping", "pulse", "bounce"],
      aspect: ["video"],
      blur: [Fo],
      breakpoint: [Fo],
      color: [OD],
      container: [Fo],
      "drop-shadow": [Fo],
      ease: ["in", "out", "in-out"],
      font: [zD],
      "font-weight": ["thin", "extralight", "light", "normal", "medium", "semibold", "bold", "extrabold", "black"],
      "inset-shadow": [Fo],
      leading: ["none", "tight", "snug", "normal", "relaxed", "loose"],
      perspective: ["dramatic", "near", "normal", "midrange", "distant", "none"],
      radius: [Fo],
      shadow: [Fo],
      spacing: ["px", Lt],
      text: [Fo],
      "text-shadow": [Fo],
      tracking: ["tighter", "tight", "normal", "wide", "wider", "widest"]
    },
    classGroups: {
      // --------------
      // --- Layout ---
      // --------------
      /**
       * Aspect Ratio
       * @see https://tailwindcss.com/docs/aspect-ratio
       */
      aspect: [{
        aspect: ["auto", "square", td, je, ze, Ae]
      }],
      /**
       * Container
       * @see https://tailwindcss.com/docs/container
       * @deprecated since Tailwind CSS v4.0.0
       */
      container: ["container"],
      /**
       * Columns
       * @see https://tailwindcss.com/docs/columns
       */
      columns: [{
        columns: [Lt, je, ze, ce]
      }],
      /**
       * Break After
       * @see https://tailwindcss.com/docs/break-after
       */
      "break-after": [{
        "break-after": Ke()
      }],
      /**
       * Break Before
       * @see https://tailwindcss.com/docs/break-before
       */
      "break-before": [{
        "break-before": Ke()
      }],
      /**
       * Break Inside
       * @see https://tailwindcss.com/docs/break-inside
       */
      "break-inside": [{
        "break-inside": ["auto", "avoid", "avoid-page", "avoid-column"]
      }],
      /**
       * Box Decoration Break
       * @see https://tailwindcss.com/docs/box-decoration-break
       */
      "box-decoration": [{
        "box-decoration": ["slice", "clone"]
      }],
      /**
       * Box Sizing
       * @see https://tailwindcss.com/docs/box-sizing
       */
      box: [{
        box: ["border", "content"]
      }],
      /**
       * Display
       * @see https://tailwindcss.com/docs/display
       */
      display: ["block", "inline-block", "inline", "flex", "inline-flex", "table", "inline-table", "table-caption", "table-cell", "table-column", "table-column-group", "table-footer-group", "table-header-group", "table-row-group", "table-row", "flow-root", "grid", "inline-grid", "contents", "list-item", "hidden"],
      /**
       * Screen Reader Only
       * @see https://tailwindcss.com/docs/display#screen-reader-only
       */
      sr: ["sr-only", "not-sr-only"],
      /**
       * Floats
       * @see https://tailwindcss.com/docs/float
       */
      float: [{
        float: ["right", "left", "none", "start", "end"]
      }],
      /**
       * Clear
       * @see https://tailwindcss.com/docs/clear
       */
      clear: [{
        clear: ["left", "right", "both", "none", "start", "end"]
      }],
      /**
       * Isolation
       * @see https://tailwindcss.com/docs/isolation
       */
      isolation: ["isolate", "isolation-auto"],
      /**
       * Object Fit
       * @see https://tailwindcss.com/docs/object-fit
       */
      "object-fit": [{
        object: ["contain", "cover", "fill", "none", "scale-down"]
      }],
      /**
       * Object Position
       * @see https://tailwindcss.com/docs/object-position
       */
      "object-position": [{
        object: ke()
      }],
      /**
       * Overflow
       * @see https://tailwindcss.com/docs/overflow
       */
      overflow: [{
        overflow: at()
      }],
      /**
       * Overflow X
       * @see https://tailwindcss.com/docs/overflow
       */
      "overflow-x": [{
        "overflow-x": at()
      }],
      /**
       * Overflow Y
       * @see https://tailwindcss.com/docs/overflow
       */
      "overflow-y": [{
        "overflow-y": at()
      }],
      /**
       * Overscroll Behavior
       * @see https://tailwindcss.com/docs/overscroll-behavior
       */
      overscroll: [{
        overscroll: Ye()
      }],
      /**
       * Overscroll Behavior X
       * @see https://tailwindcss.com/docs/overscroll-behavior
       */
      "overscroll-x": [{
        "overscroll-x": Ye()
      }],
      /**
       * Overscroll Behavior Y
       * @see https://tailwindcss.com/docs/overscroll-behavior
       */
      "overscroll-y": [{
        "overscroll-y": Ye()
      }],
      /**
       * Position
       * @see https://tailwindcss.com/docs/position
       */
      position: ["static", "fixed", "absolute", "relative", "sticky"],
      /**
       * Top / Right / Bottom / Left
       * @see https://tailwindcss.com/docs/top-right-bottom-left
       */
      inset: [{
        inset: Oe()
      }],
      /**
       * Right / Left
       * @see https://tailwindcss.com/docs/top-right-bottom-left
       */
      "inset-x": [{
        "inset-x": Oe()
      }],
      /**
       * Top / Bottom
       * @see https://tailwindcss.com/docs/top-right-bottom-left
       */
      "inset-y": [{
        "inset-y": Oe()
      }],
      /**
       * Start
       * @see https://tailwindcss.com/docs/top-right-bottom-left
       */
      start: [{
        start: Oe()
      }],
      /**
       * End
       * @see https://tailwindcss.com/docs/top-right-bottom-left
       */
      end: [{
        end: Oe()
      }],
      /**
       * Top
       * @see https://tailwindcss.com/docs/top-right-bottom-left
       */
      top: [{
        top: Oe()
      }],
      /**
       * Right
       * @see https://tailwindcss.com/docs/top-right-bottom-left
       */
      right: [{
        right: Oe()
      }],
      /**
       * Bottom
       * @see https://tailwindcss.com/docs/top-right-bottom-left
       */
      bottom: [{
        bottom: Oe()
      }],
      /**
       * Left
       * @see https://tailwindcss.com/docs/top-right-bottom-left
       */
      left: [{
        left: Oe()
      }],
      /**
       * Visibility
       * @see https://tailwindcss.com/docs/visibility
       */
      visibility: ["visible", "invisible", "collapse"],
      /**
       * Z-Index
       * @see https://tailwindcss.com/docs/z-index
       */
      z: [{
        z: [Ju, "auto", ze, je]
      }],
      // ------------------------
      // --- Flexbox and Grid ---
      // ------------------------
      /**
       * Flex Basis
       * @see https://tailwindcss.com/docs/flex-basis
       */
      basis: [{
        basis: [td, "full", "auto", ce, ...be()]
      }],
      /**
       * Flex Direction
       * @see https://tailwindcss.com/docs/flex-direction
       */
      "flex-direction": [{
        flex: ["row", "row-reverse", "col", "col-reverse"]
      }],
      /**
       * Flex Wrap
       * @see https://tailwindcss.com/docs/flex-wrap
       */
      "flex-wrap": [{
        flex: ["nowrap", "wrap", "wrap-reverse"]
      }],
      /**
       * Flex
       * @see https://tailwindcss.com/docs/flex
       */
      flex: [{
        flex: [Lt, td, "auto", "initial", "none", je]
      }],
      /**
       * Flex Grow
       * @see https://tailwindcss.com/docs/flex-grow
       */
      grow: [{
        grow: ["", Lt, ze, je]
      }],
      /**
       * Flex Shrink
       * @see https://tailwindcss.com/docs/flex-shrink
       */
      shrink: [{
        shrink: ["", Lt, ze, je]
      }],
      /**
       * Order
       * @see https://tailwindcss.com/docs/order
       */
      order: [{
        order: [Ju, "first", "last", "none", ze, je]
      }],
      /**
       * Grid Template Columns
       * @see https://tailwindcss.com/docs/grid-template-columns
       */
      "grid-cols": [{
        "grid-cols": $e()
      }],
      /**
       * Grid Column Start / End
       * @see https://tailwindcss.com/docs/grid-column
       */
      "col-start-end": [{
        col: it()
      }],
      /**
       * Grid Column Start
       * @see https://tailwindcss.com/docs/grid-column
       */
      "col-start": [{
        "col-start": Rt()
      }],
      /**
       * Grid Column End
       * @see https://tailwindcss.com/docs/grid-column
       */
      "col-end": [{
        "col-end": Rt()
      }],
      /**
       * Grid Template Rows
       * @see https://tailwindcss.com/docs/grid-template-rows
       */
      "grid-rows": [{
        "grid-rows": $e()
      }],
      /**
       * Grid Row Start / End
       * @see https://tailwindcss.com/docs/grid-row
       */
      "row-start-end": [{
        row: it()
      }],
      /**
       * Grid Row Start
       * @see https://tailwindcss.com/docs/grid-row
       */
      "row-start": [{
        "row-start": Rt()
      }],
      /**
       * Grid Row End
       * @see https://tailwindcss.com/docs/grid-row
       */
      "row-end": [{
        "row-end": Rt()
      }],
      /**
       * Grid Auto Flow
       * @see https://tailwindcss.com/docs/grid-auto-flow
       */
      "grid-flow": [{
        "grid-flow": ["row", "col", "dense", "row-dense", "col-dense"]
      }],
      /**
       * Grid Auto Columns
       * @see https://tailwindcss.com/docs/grid-auto-columns
       */
      "auto-cols": [{
        "auto-cols": Ie()
      }],
      /**
       * Grid Auto Rows
       * @see https://tailwindcss.com/docs/grid-auto-rows
       */
      "auto-rows": [{
        "auto-rows": Ie()
      }],
      /**
       * Gap
       * @see https://tailwindcss.com/docs/gap
       */
      gap: [{
        gap: be()
      }],
      /**
       * Gap X
       * @see https://tailwindcss.com/docs/gap
       */
      "gap-x": [{
        "gap-x": be()
      }],
      /**
       * Gap Y
       * @see https://tailwindcss.com/docs/gap
       */
      "gap-y": [{
        "gap-y": be()
      }],
      /**
       * Justify Content
       * @see https://tailwindcss.com/docs/justify-content
       */
      "justify-content": [{
        justify: [...st(), "normal"]
      }],
      /**
       * Justify Items
       * @see https://tailwindcss.com/docs/justify-items
       */
      "justify-items": [{
        "justify-items": [...Nt(), "normal"]
      }],
      /**
       * Justify Self
       * @see https://tailwindcss.com/docs/justify-self
       */
      "justify-self": [{
        "justify-self": ["auto", ...Nt()]
      }],
      /**
       * Align Content
       * @see https://tailwindcss.com/docs/align-content
       */
      "align-content": [{
        content: ["normal", ...st()]
      }],
      /**
       * Align Items
       * @see https://tailwindcss.com/docs/align-items
       */
      "align-items": [{
        items: [...Nt(), {
          baseline: ["", "last"]
        }]
      }],
      /**
       * Align Self
       * @see https://tailwindcss.com/docs/align-self
       */
      "align-self": [{
        self: ["auto", ...Nt(), {
          baseline: ["", "last"]
        }]
      }],
      /**
       * Place Content
       * @see https://tailwindcss.com/docs/place-content
       */
      "place-content": [{
        "place-content": st()
      }],
      /**
       * Place Items
       * @see https://tailwindcss.com/docs/place-items
       */
      "place-items": [{
        "place-items": [...Nt(), "baseline"]
      }],
      /**
       * Place Self
       * @see https://tailwindcss.com/docs/place-self
       */
      "place-self": [{
        "place-self": ["auto", ...Nt()]
      }],
      // Spacing
      /**
       * Padding
       * @see https://tailwindcss.com/docs/padding
       */
      p: [{
        p: be()
      }],
      /**
       * Padding X
       * @see https://tailwindcss.com/docs/padding
       */
      px: [{
        px: be()
      }],
      /**
       * Padding Y
       * @see https://tailwindcss.com/docs/padding
       */
      py: [{
        py: be()
      }],
      /**
       * Padding Start
       * @see https://tailwindcss.com/docs/padding
       */
      ps: [{
        ps: be()
      }],
      /**
       * Padding End
       * @see https://tailwindcss.com/docs/padding
       */
      pe: [{
        pe: be()
      }],
      /**
       * Padding Top
       * @see https://tailwindcss.com/docs/padding
       */
      pt: [{
        pt: be()
      }],
      /**
       * Padding Right
       * @see https://tailwindcss.com/docs/padding
       */
      pr: [{
        pr: be()
      }],
      /**
       * Padding Bottom
       * @see https://tailwindcss.com/docs/padding
       */
      pb: [{
        pb: be()
      }],
      /**
       * Padding Left
       * @see https://tailwindcss.com/docs/padding
       */
      pl: [{
        pl: be()
      }],
      /**
       * Margin
       * @see https://tailwindcss.com/docs/margin
       */
      m: [{
        m: yt()
      }],
      /**
       * Margin X
       * @see https://tailwindcss.com/docs/margin
       */
      mx: [{
        mx: yt()
      }],
      /**
       * Margin Y
       * @see https://tailwindcss.com/docs/margin
       */
      my: [{
        my: yt()
      }],
      /**
       * Margin Start
       * @see https://tailwindcss.com/docs/margin
       */
      ms: [{
        ms: yt()
      }],
      /**
       * Margin End
       * @see https://tailwindcss.com/docs/margin
       */
      me: [{
        me: yt()
      }],
      /**
       * Margin Top
       * @see https://tailwindcss.com/docs/margin
       */
      mt: [{
        mt: yt()
      }],
      /**
       * Margin Right
       * @see https://tailwindcss.com/docs/margin
       */
      mr: [{
        mr: yt()
      }],
      /**
       * Margin Bottom
       * @see https://tailwindcss.com/docs/margin
       */
      mb: [{
        mb: yt()
      }],
      /**
       * Margin Left
       * @see https://tailwindcss.com/docs/margin
       */
      ml: [{
        ml: yt()
      }],
      /**
       * Space Between X
       * @see https://tailwindcss.com/docs/margin#adding-space-between-children
       */
      "space-x": [{
        "space-x": be()
      }],
      /**
       * Space Between X Reverse
       * @see https://tailwindcss.com/docs/margin#adding-space-between-children
       */
      "space-x-reverse": ["space-x-reverse"],
      /**
       * Space Between Y
       * @see https://tailwindcss.com/docs/margin#adding-space-between-children
       */
      "space-y": [{
        "space-y": be()
      }],
      /**
       * Space Between Y Reverse
       * @see https://tailwindcss.com/docs/margin#adding-space-between-children
       */
      "space-y-reverse": ["space-y-reverse"],
      // --------------
      // --- Sizing ---
      // --------------
      /**
       * Size
       * @see https://tailwindcss.com/docs/width#setting-both-width-and-height
       */
      size: [{
        size: Se()
      }],
      /**
       * Width
       * @see https://tailwindcss.com/docs/width
       */
      w: [{
        w: [ce, "screen", ...Se()]
      }],
      /**
       * Min-Width
       * @see https://tailwindcss.com/docs/min-width
       */
      "min-w": [{
        "min-w": [
          ce,
          "screen",
          /** Deprecated. @see https://github.com/tailwindlabs/tailwindcss.com/issues/2027#issuecomment-2620152757 */
          "none",
          ...Se()
        ]
      }],
      /**
       * Max-Width
       * @see https://tailwindcss.com/docs/max-width
       */
      "max-w": [{
        "max-w": [
          ce,
          "screen",
          "none",
          /** Deprecated since Tailwind CSS v4.0.0. @see https://github.com/tailwindlabs/tailwindcss.com/issues/2027#issuecomment-2620152757 */
          "prose",
          /** Deprecated since Tailwind CSS v4.0.0. @see https://github.com/tailwindlabs/tailwindcss.com/issues/2027#issuecomment-2620152757 */
          {
            screen: [y]
          },
          ...Se()
        ]
      }],
      /**
       * Height
       * @see https://tailwindcss.com/docs/height
       */
      h: [{
        h: ["screen", "lh", ...Se()]
      }],
      /**
       * Min-Height
       * @see https://tailwindcss.com/docs/min-height
       */
      "min-h": [{
        "min-h": ["screen", "lh", "none", ...Se()]
      }],
      /**
       * Max-Height
       * @see https://tailwindcss.com/docs/max-height
       */
      "max-h": [{
        "max-h": ["screen", "lh", ...Se()]
      }],
      // ------------------
      // --- Typography ---
      // ------------------
      /**
       * Font Size
       * @see https://tailwindcss.com/docs/font-size
       */
      "font-size": [{
        text: ["base", b, dv, ic]
      }],
      /**
       * Font Smoothing
       * @see https://tailwindcss.com/docs/font-smoothing
       */
      "font-smoothing": ["antialiased", "subpixel-antialiased"],
      /**
       * Font Style
       * @see https://tailwindcss.com/docs/font-style
       */
      "font-style": ["italic", "not-italic"],
      /**
       * Font Weight
       * @see https://tailwindcss.com/docs/font-weight
       */
      "font-weight": [{
        font: [U, ze, US]
      }],
      /**
       * Font Stretch
       * @see https://tailwindcss.com/docs/font-stretch
       */
      "font-stretch": [{
        "font-stretch": ["ultra-condensed", "extra-condensed", "condensed", "semi-condensed", "normal", "semi-expanded", "expanded", "extra-expanded", "ultra-expanded", AS, je]
      }],
      /**
       * Font Family
       * @see https://tailwindcss.com/docs/font-family
       */
      "font-family": [{
        font: [FD, je, w]
      }],
      /**
       * Font Variant Numeric
       * @see https://tailwindcss.com/docs/font-variant-numeric
       */
      "fvn-normal": ["normal-nums"],
      /**
       * Font Variant Numeric
       * @see https://tailwindcss.com/docs/font-variant-numeric
       */
      "fvn-ordinal": ["ordinal"],
      /**
       * Font Variant Numeric
       * @see https://tailwindcss.com/docs/font-variant-numeric
       */
      "fvn-slashed-zero": ["slashed-zero"],
      /**
       * Font Variant Numeric
       * @see https://tailwindcss.com/docs/font-variant-numeric
       */
      "fvn-figure": ["lining-nums", "oldstyle-nums"],
      /**
       * Font Variant Numeric
       * @see https://tailwindcss.com/docs/font-variant-numeric
       */
      "fvn-spacing": ["proportional-nums", "tabular-nums"],
      /**
       * Font Variant Numeric
       * @see https://tailwindcss.com/docs/font-variant-numeric
       */
      "fvn-fraction": ["diagonal-fractions", "stacked-fractions"],
      /**
       * Letter Spacing
       * @see https://tailwindcss.com/docs/letter-spacing
       */
      tracking: [{
        tracking: [X, ze, je]
      }],
      /**
       * Line Clamp
       * @see https://tailwindcss.com/docs/line-clamp
       */
      "line-clamp": [{
        "line-clamp": [Lt, "none", ze, US]
      }],
      /**
       * Line Height
       * @see https://tailwindcss.com/docs/line-height
       */
      leading: [{
        leading: [
          /** Deprecated since Tailwind CSS v4.0.0. @see https://github.com/tailwindlabs/tailwindcss.com/issues/2027#issuecomment-2620152757 */
          W,
          ...be()
        ]
      }],
      /**
       * List Style Image
       * @see https://tailwindcss.com/docs/list-style-image
       */
      "list-image": [{
        "list-image": ["none", ze, je]
      }],
      /**
       * List Style Position
       * @see https://tailwindcss.com/docs/list-style-position
       */
      "list-style-position": [{
        list: ["inside", "outside"]
      }],
      /**
       * List Style Type
       * @see https://tailwindcss.com/docs/list-style-type
       */
      "list-style-type": [{
        list: ["disc", "decimal", "none", ze, je]
      }],
      /**
       * Text Alignment
       * @see https://tailwindcss.com/docs/text-align
       */
      "text-alignment": [{
        text: ["left", "center", "right", "justify", "start", "end"]
      }],
      /**
       * Placeholder Color
       * @deprecated since Tailwind CSS v3.0.0
       * @see https://v3.tailwindcss.com/docs/placeholder-color
       */
      "placeholder-color": [{
        placeholder: I()
      }],
      /**
       * Text Color
       * @see https://tailwindcss.com/docs/text-color
       */
      "text-color": [{
        text: I()
      }],
      /**
       * Text Decoration
       * @see https://tailwindcss.com/docs/text-decoration
       */
      "text-decoration": ["underline", "overline", "line-through", "no-underline"],
      /**
       * Text Decoration Style
       * @see https://tailwindcss.com/docs/text-decoration-style
       */
      "text-decoration-style": [{
        decoration: [...ft(), "wavy"]
      }],
      /**
       * Text Decoration Thickness
       * @see https://tailwindcss.com/docs/text-decoration-thickness
       */
      "text-decoration-thickness": [{
        decoration: [Lt, "from-font", "auto", ze, ic]
      }],
      /**
       * Text Decoration Color
       * @see https://tailwindcss.com/docs/text-decoration-color
       */
      "text-decoration-color": [{
        decoration: I()
      }],
      /**
       * Text Underline Offset
       * @see https://tailwindcss.com/docs/text-underline-offset
       */
      "underline-offset": [{
        "underline-offset": [Lt, "auto", ze, je]
      }],
      /**
       * Text Transform
       * @see https://tailwindcss.com/docs/text-transform
       */
      "text-transform": ["uppercase", "lowercase", "capitalize", "normal-case"],
      /**
       * Text Overflow
       * @see https://tailwindcss.com/docs/text-overflow
       */
      "text-overflow": ["truncate", "text-ellipsis", "text-clip"],
      /**
       * Text Wrap
       * @see https://tailwindcss.com/docs/text-wrap
       */
      "text-wrap": [{
        text: ["wrap", "nowrap", "balance", "pretty"]
      }],
      /**
       * Text Indent
       * @see https://tailwindcss.com/docs/text-indent
       */
      indent: [{
        indent: be()
      }],
      /**
       * Vertical Alignment
       * @see https://tailwindcss.com/docs/vertical-align
       */
      "vertical-align": [{
        align: ["baseline", "top", "middle", "bottom", "text-top", "text-bottom", "sub", "super", ze, je]
      }],
      /**
       * Whitespace
       * @see https://tailwindcss.com/docs/whitespace
       */
      whitespace: [{
        whitespace: ["normal", "nowrap", "pre", "pre-line", "pre-wrap", "break-spaces"]
      }],
      /**
       * Word Break
       * @see https://tailwindcss.com/docs/word-break
       */
      break: [{
        break: ["normal", "words", "all", "keep"]
      }],
      /**
       * Overflow Wrap
       * @see https://tailwindcss.com/docs/overflow-wrap
       */
      wrap: [{
        wrap: ["break-word", "anywhere", "normal"]
      }],
      /**
       * Hyphens
       * @see https://tailwindcss.com/docs/hyphens
       */
      hyphens: [{
        hyphens: ["none", "manual", "auto"]
      }],
      /**
       * Content
       * @see https://tailwindcss.com/docs/content
       */
      content: [{
        content: ["none", ze, je]
      }],
      // -------------------
      // --- Backgrounds ---
      // -------------------
      /**
       * Background Attachment
       * @see https://tailwindcss.com/docs/background-attachment
       */
      "bg-attachment": [{
        bg: ["fixed", "local", "scroll"]
      }],
      /**
       * Background Clip
       * @see https://tailwindcss.com/docs/background-clip
       */
      "bg-clip": [{
        "bg-clip": ["border", "padding", "content", "text"]
      }],
      /**
       * Background Origin
       * @see https://tailwindcss.com/docs/background-origin
       */
      "bg-origin": [{
        "bg-origin": ["border", "padding", "content"]
      }],
      /**
       * Background Position
       * @see https://tailwindcss.com/docs/background-position
       */
      "bg-position": [{
        bg: Ue()
      }],
      /**
       * Background Repeat
       * @see https://tailwindcss.com/docs/background-repeat
       */
      "bg-repeat": [{
        bg: pe()
      }],
      /**
       * Background Size
       * @see https://tailwindcss.com/docs/background-size
       */
      "bg-size": [{
        bg: O()
      }],
      /**
       * Background Image
       * @see https://tailwindcss.com/docs/background-image
       */
      "bg-image": [{
        bg: ["none", {
          linear: [{
            to: ["t", "tr", "r", "br", "b", "bl", "l", "tl"]
          }, Ju, ze, je],
          radial: ["", ze, je],
          conic: [Ju, ze, je]
        }, PD, UD]
      }],
      /**
       * Background Color
       * @see https://tailwindcss.com/docs/background-color
       */
      "bg-color": [{
        bg: I()
      }],
      /**
       * Gradient Color Stops From Position
       * @see https://tailwindcss.com/docs/gradient-color-stops
       */
      "gradient-from-pos": [{
        from: q()
      }],
      /**
       * Gradient Color Stops Via Position
       * @see https://tailwindcss.com/docs/gradient-color-stops
       */
      "gradient-via-pos": [{
        via: q()
      }],
      /**
       * Gradient Color Stops To Position
       * @see https://tailwindcss.com/docs/gradient-color-stops
       */
      "gradient-to-pos": [{
        to: q()
      }],
      /**
       * Gradient Color Stops From
       * @see https://tailwindcss.com/docs/gradient-color-stops
       */
      "gradient-from": [{
        from: I()
      }],
      /**
       * Gradient Color Stops Via
       * @see https://tailwindcss.com/docs/gradient-color-stops
       */
      "gradient-via": [{
        via: I()
      }],
      /**
       * Gradient Color Stops To
       * @see https://tailwindcss.com/docs/gradient-color-stops
       */
      "gradient-to": [{
        to: I()
      }],
      // ---------------
      // --- Borders ---
      // ---------------
      /**
       * Border Radius
       * @see https://tailwindcss.com/docs/border-radius
       */
      rounded: [{
        rounded: Re()
      }],
      /**
       * Border Radius Start
       * @see https://tailwindcss.com/docs/border-radius
       */
      "rounded-s": [{
        "rounded-s": Re()
      }],
      /**
       * Border Radius End
       * @see https://tailwindcss.com/docs/border-radius
       */
      "rounded-e": [{
        "rounded-e": Re()
      }],
      /**
       * Border Radius Top
       * @see https://tailwindcss.com/docs/border-radius
       */
      "rounded-t": [{
        "rounded-t": Re()
      }],
      /**
       * Border Radius Right
       * @see https://tailwindcss.com/docs/border-radius
       */
      "rounded-r": [{
        "rounded-r": Re()
      }],
      /**
       * Border Radius Bottom
       * @see https://tailwindcss.com/docs/border-radius
       */
      "rounded-b": [{
        "rounded-b": Re()
      }],
      /**
       * Border Radius Left
       * @see https://tailwindcss.com/docs/border-radius
       */
      "rounded-l": [{
        "rounded-l": Re()
      }],
      /**
       * Border Radius Start Start
       * @see https://tailwindcss.com/docs/border-radius
       */
      "rounded-ss": [{
        "rounded-ss": Re()
      }],
      /**
       * Border Radius Start End
       * @see https://tailwindcss.com/docs/border-radius
       */
      "rounded-se": [{
        "rounded-se": Re()
      }],
      /**
       * Border Radius End End
       * @see https://tailwindcss.com/docs/border-radius
       */
      "rounded-ee": [{
        "rounded-ee": Re()
      }],
      /**
       * Border Radius End Start
       * @see https://tailwindcss.com/docs/border-radius
       */
      "rounded-es": [{
        "rounded-es": Re()
      }],
      /**
       * Border Radius Top Left
       * @see https://tailwindcss.com/docs/border-radius
       */
      "rounded-tl": [{
        "rounded-tl": Re()
      }],
      /**
       * Border Radius Top Right
       * @see https://tailwindcss.com/docs/border-radius
       */
      "rounded-tr": [{
        "rounded-tr": Re()
      }],
      /**
       * Border Radius Bottom Right
       * @see https://tailwindcss.com/docs/border-radius
       */
      "rounded-br": [{
        "rounded-br": Re()
      }],
      /**
       * Border Radius Bottom Left
       * @see https://tailwindcss.com/docs/border-radius
       */
      "rounded-bl": [{
        "rounded-bl": Re()
      }],
      /**
       * Border Width
       * @see https://tailwindcss.com/docs/border-width
       */
      "border-w": [{
        border: Me()
      }],
      /**
       * Border Width X
       * @see https://tailwindcss.com/docs/border-width
       */
      "border-w-x": [{
        "border-x": Me()
      }],
      /**
       * Border Width Y
       * @see https://tailwindcss.com/docs/border-width
       */
      "border-w-y": [{
        "border-y": Me()
      }],
      /**
       * Border Width Start
       * @see https://tailwindcss.com/docs/border-width
       */
      "border-w-s": [{
        "border-s": Me()
      }],
      /**
       * Border Width End
       * @see https://tailwindcss.com/docs/border-width
       */
      "border-w-e": [{
        "border-e": Me()
      }],
      /**
       * Border Width Top
       * @see https://tailwindcss.com/docs/border-width
       */
      "border-w-t": [{
        "border-t": Me()
      }],
      /**
       * Border Width Right
       * @see https://tailwindcss.com/docs/border-width
       */
      "border-w-r": [{
        "border-r": Me()
      }],
      /**
       * Border Width Bottom
       * @see https://tailwindcss.com/docs/border-width
       */
      "border-w-b": [{
        "border-b": Me()
      }],
      /**
       * Border Width Left
       * @see https://tailwindcss.com/docs/border-width
       */
      "border-w-l": [{
        "border-l": Me()
      }],
      /**
       * Divide Width X
       * @see https://tailwindcss.com/docs/border-width#between-children
       */
      "divide-x": [{
        "divide-x": Me()
      }],
      /**
       * Divide Width X Reverse
       * @see https://tailwindcss.com/docs/border-width#between-children
       */
      "divide-x-reverse": ["divide-x-reverse"],
      /**
       * Divide Width Y
       * @see https://tailwindcss.com/docs/border-width#between-children
       */
      "divide-y": [{
        "divide-y": Me()
      }],
      /**
       * Divide Width Y Reverse
       * @see https://tailwindcss.com/docs/border-width#between-children
       */
      "divide-y-reverse": ["divide-y-reverse"],
      /**
       * Border Style
       * @see https://tailwindcss.com/docs/border-style
       */
      "border-style": [{
        border: [...ft(), "hidden", "none"]
      }],
      /**
       * Divide Style
       * @see https://tailwindcss.com/docs/border-style#setting-the-divider-style
       */
      "divide-style": [{
        divide: [...ft(), "hidden", "none"]
      }],
      /**
       * Border Color
       * @see https://tailwindcss.com/docs/border-color
       */
      "border-color": [{
        border: I()
      }],
      /**
       * Border Color X
       * @see https://tailwindcss.com/docs/border-color
       */
      "border-color-x": [{
        "border-x": I()
      }],
      /**
       * Border Color Y
       * @see https://tailwindcss.com/docs/border-color
       */
      "border-color-y": [{
        "border-y": I()
      }],
      /**
       * Border Color S
       * @see https://tailwindcss.com/docs/border-color
       */
      "border-color-s": [{
        "border-s": I()
      }],
      /**
       * Border Color E
       * @see https://tailwindcss.com/docs/border-color
       */
      "border-color-e": [{
        "border-e": I()
      }],
      /**
       * Border Color Top
       * @see https://tailwindcss.com/docs/border-color
       */
      "border-color-t": [{
        "border-t": I()
      }],
      /**
       * Border Color Right
       * @see https://tailwindcss.com/docs/border-color
       */
      "border-color-r": [{
        "border-r": I()
      }],
      /**
       * Border Color Bottom
       * @see https://tailwindcss.com/docs/border-color
       */
      "border-color-b": [{
        "border-b": I()
      }],
      /**
       * Border Color Left
       * @see https://tailwindcss.com/docs/border-color
       */
      "border-color-l": [{
        "border-l": I()
      }],
      /**
       * Divide Color
       * @see https://tailwindcss.com/docs/divide-color
       */
      "divide-color": [{
        divide: I()
      }],
      /**
       * Outline Style
       * @see https://tailwindcss.com/docs/outline-style
       */
      "outline-style": [{
        outline: [...ft(), "none", "hidden"]
      }],
      /**
       * Outline Offset
       * @see https://tailwindcss.com/docs/outline-offset
       */
      "outline-offset": [{
        "outline-offset": [Lt, ze, je]
      }],
      /**
       * Outline Width
       * @see https://tailwindcss.com/docs/outline-width
       */
      "outline-w": [{
        outline: ["", Lt, dv, ic]
      }],
      /**
       * Outline Color
       * @see https://tailwindcss.com/docs/outline-color
       */
      "outline-color": [{
        outline: I()
      }],
      // ---------------
      // --- Effects ---
      // ---------------
      /**
       * Box Shadow
       * @see https://tailwindcss.com/docs/box-shadow
       */
      shadow: [{
        shadow: [
          // Deprecated since Tailwind CSS v4.0.0
          "",
          "none",
          ye,
          uy,
          oy
        ]
      }],
      /**
       * Box Shadow Color
       * @see https://tailwindcss.com/docs/box-shadow#setting-the-shadow-color
       */
      "shadow-color": [{
        shadow: I()
      }],
      /**
       * Inset Box Shadow
       * @see https://tailwindcss.com/docs/box-shadow#adding-an-inset-shadow
       */
      "inset-shadow": [{
        "inset-shadow": ["none", ne, uy, oy]
      }],
      /**
       * Inset Box Shadow Color
       * @see https://tailwindcss.com/docs/box-shadow#setting-the-inset-shadow-color
       */
      "inset-shadow-color": [{
        "inset-shadow": I()
      }],
      /**
       * Ring Width
       * @see https://tailwindcss.com/docs/box-shadow#adding-a-ring
       */
      "ring-w": [{
        ring: Me()
      }],
      /**
       * Ring Width Inset
       * @see https://v3.tailwindcss.com/docs/ring-width#inset-rings
       * @deprecated since Tailwind CSS v4.0.0
       * @see https://github.com/tailwindlabs/tailwindcss/blob/v4.0.0/packages/tailwindcss/src/utilities.ts#L4158
       */
      "ring-w-inset": ["ring-inset"],
      /**
       * Ring Color
       * @see https://tailwindcss.com/docs/box-shadow#setting-the-ring-color
       */
      "ring-color": [{
        ring: I()
      }],
      /**
       * Ring Offset Width
       * @see https://v3.tailwindcss.com/docs/ring-offset-width
       * @deprecated since Tailwind CSS v4.0.0
       * @see https://github.com/tailwindlabs/tailwindcss/blob/v4.0.0/packages/tailwindcss/src/utilities.ts#L4158
       */
      "ring-offset-w": [{
        "ring-offset": [Lt, ic]
      }],
      /**
       * Ring Offset Color
       * @see https://v3.tailwindcss.com/docs/ring-offset-color
       * @deprecated since Tailwind CSS v4.0.0
       * @see https://github.com/tailwindlabs/tailwindcss/blob/v4.0.0/packages/tailwindcss/src/utilities.ts#L4158
       */
      "ring-offset-color": [{
        "ring-offset": I()
      }],
      /**
       * Inset Ring Width
       * @see https://tailwindcss.com/docs/box-shadow#adding-an-inset-ring
       */
      "inset-ring-w": [{
        "inset-ring": Me()
      }],
      /**
       * Inset Ring Color
       * @see https://tailwindcss.com/docs/box-shadow#setting-the-inset-ring-color
       */
      "inset-ring-color": [{
        "inset-ring": I()
      }],
      /**
       * Text Shadow
       * @see https://tailwindcss.com/docs/text-shadow
       */
      "text-shadow": [{
        "text-shadow": ["none", oe, uy, oy]
      }],
      /**
       * Text Shadow Color
       * @see https://tailwindcss.com/docs/text-shadow#setting-the-shadow-color
       */
      "text-shadow-color": [{
        "text-shadow": I()
      }],
      /**
       * Opacity
       * @see https://tailwindcss.com/docs/opacity
       */
      opacity: [{
        opacity: [Lt, ze, je]
      }],
      /**
       * Mix Blend Mode
       * @see https://tailwindcss.com/docs/mix-blend-mode
       */
      "mix-blend": [{
        "mix-blend": [...vt(), "plus-darker", "plus-lighter"]
      }],
      /**
       * Background Blend Mode
       * @see https://tailwindcss.com/docs/background-blend-mode
       */
      "bg-blend": [{
        "bg-blend": vt()
      }],
      /**
       * Mask Clip
       * @see https://tailwindcss.com/docs/mask-clip
       */
      "mask-clip": [{
        "mask-clip": ["border", "padding", "content", "fill", "stroke", "view"]
      }, "mask-no-clip"],
      /**
       * Mask Composite
       * @see https://tailwindcss.com/docs/mask-composite
       */
      "mask-composite": [{
        mask: ["add", "subtract", "intersect", "exclude"]
      }],
      /**
       * Mask Image
       * @see https://tailwindcss.com/docs/mask-image
       */
      "mask-image-linear-pos": [{
        "mask-linear": [Lt]
      }],
      "mask-image-linear-from-pos": [{
        "mask-linear-from": Ge()
      }],
      "mask-image-linear-to-pos": [{
        "mask-linear-to": Ge()
      }],
      "mask-image-linear-from-color": [{
        "mask-linear-from": I()
      }],
      "mask-image-linear-to-color": [{
        "mask-linear-to": I()
      }],
      "mask-image-t-from-pos": [{
        "mask-t-from": Ge()
      }],
      "mask-image-t-to-pos": [{
        "mask-t-to": Ge()
      }],
      "mask-image-t-from-color": [{
        "mask-t-from": I()
      }],
      "mask-image-t-to-color": [{
        "mask-t-to": I()
      }],
      "mask-image-r-from-pos": [{
        "mask-r-from": Ge()
      }],
      "mask-image-r-to-pos": [{
        "mask-r-to": Ge()
      }],
      "mask-image-r-from-color": [{
        "mask-r-from": I()
      }],
      "mask-image-r-to-color": [{
        "mask-r-to": I()
      }],
      "mask-image-b-from-pos": [{
        "mask-b-from": Ge()
      }],
      "mask-image-b-to-pos": [{
        "mask-b-to": Ge()
      }],
      "mask-image-b-from-color": [{
        "mask-b-from": I()
      }],
      "mask-image-b-to-color": [{
        "mask-b-to": I()
      }],
      "mask-image-l-from-pos": [{
        "mask-l-from": Ge()
      }],
      "mask-image-l-to-pos": [{
        "mask-l-to": Ge()
      }],
      "mask-image-l-from-color": [{
        "mask-l-from": I()
      }],
      "mask-image-l-to-color": [{
        "mask-l-to": I()
      }],
      "mask-image-x-from-pos": [{
        "mask-x-from": Ge()
      }],
      "mask-image-x-to-pos": [{
        "mask-x-to": Ge()
      }],
      "mask-image-x-from-color": [{
        "mask-x-from": I()
      }],
      "mask-image-x-to-color": [{
        "mask-x-to": I()
      }],
      "mask-image-y-from-pos": [{
        "mask-y-from": Ge()
      }],
      "mask-image-y-to-pos": [{
        "mask-y-to": Ge()
      }],
      "mask-image-y-from-color": [{
        "mask-y-from": I()
      }],
      "mask-image-y-to-color": [{
        "mask-y-to": I()
      }],
      "mask-image-radial": [{
        "mask-radial": [ze, je]
      }],
      "mask-image-radial-from-pos": [{
        "mask-radial-from": Ge()
      }],
      "mask-image-radial-to-pos": [{
        "mask-radial-to": Ge()
      }],
      "mask-image-radial-from-color": [{
        "mask-radial-from": I()
      }],
      "mask-image-radial-to-color": [{
        "mask-radial-to": I()
      }],
      "mask-image-radial-shape": [{
        "mask-radial": ["circle", "ellipse"]
      }],
      "mask-image-radial-size": [{
        "mask-radial": [{
          closest: ["side", "corner"],
          farthest: ["side", "corner"]
        }]
      }],
      "mask-image-radial-pos": [{
        "mask-radial-at": ct()
      }],
      "mask-image-conic-pos": [{
        "mask-conic": [Lt]
      }],
      "mask-image-conic-from-pos": [{
        "mask-conic-from": Ge()
      }],
      "mask-image-conic-to-pos": [{
        "mask-conic-to": Ge()
      }],
      "mask-image-conic-from-color": [{
        "mask-conic-from": I()
      }],
      "mask-image-conic-to-color": [{
        "mask-conic-to": I()
      }],
      /**
       * Mask Mode
       * @see https://tailwindcss.com/docs/mask-mode
       */
      "mask-mode": [{
        mask: ["alpha", "luminance", "match"]
      }],
      /**
       * Mask Origin
       * @see https://tailwindcss.com/docs/mask-origin
       */
      "mask-origin": [{
        "mask-origin": ["border", "padding", "content", "fill", "stroke", "view"]
      }],
      /**
       * Mask Position
       * @see https://tailwindcss.com/docs/mask-position
       */
      "mask-position": [{
        mask: Ue()
      }],
      /**
       * Mask Repeat
       * @see https://tailwindcss.com/docs/mask-repeat
       */
      "mask-repeat": [{
        mask: pe()
      }],
      /**
       * Mask Size
       * @see https://tailwindcss.com/docs/mask-size
       */
      "mask-size": [{
        mask: O()
      }],
      /**
       * Mask Type
       * @see https://tailwindcss.com/docs/mask-type
       */
      "mask-type": [{
        "mask-type": ["alpha", "luminance"]
      }],
      /**
       * Mask Image
       * @see https://tailwindcss.com/docs/mask-image
       */
      "mask-image": [{
        mask: ["none", ze, je]
      }],
      // ---------------
      // --- Filters ---
      // ---------------
      /**
       * Filter
       * @see https://tailwindcss.com/docs/filter
       */
      filter: [{
        filter: [
          // Deprecated since Tailwind CSS v3.0.0
          "",
          "none",
          ze,
          je
        ]
      }],
      /**
       * Blur
       * @see https://tailwindcss.com/docs/blur
       */
      blur: [{
        blur: St()
      }],
      /**
       * Brightness
       * @see https://tailwindcss.com/docs/brightness
       */
      brightness: [{
        brightness: [Lt, ze, je]
      }],
      /**
       * Contrast
       * @see https://tailwindcss.com/docs/contrast
       */
      contrast: [{
        contrast: [Lt, ze, je]
      }],
      /**
       * Drop Shadow
       * @see https://tailwindcss.com/docs/drop-shadow
       */
      "drop-shadow": [{
        "drop-shadow": [
          // Deprecated since Tailwind CSS v4.0.0
          "",
          "none",
          V,
          uy,
          oy
        ]
      }],
      /**
       * Drop Shadow Color
       * @see https://tailwindcss.com/docs/filter-drop-shadow#setting-the-shadow-color
       */
      "drop-shadow-color": [{
        "drop-shadow": I()
      }],
      /**
       * Grayscale
       * @see https://tailwindcss.com/docs/grayscale
       */
      grayscale: [{
        grayscale: ["", Lt, ze, je]
      }],
      /**
       * Hue Rotate
       * @see https://tailwindcss.com/docs/hue-rotate
       */
      "hue-rotate": [{
        "hue-rotate": [Lt, ze, je]
      }],
      /**
       * Invert
       * @see https://tailwindcss.com/docs/invert
       */
      invert: [{
        invert: ["", Lt, ze, je]
      }],
      /**
       * Saturate
       * @see https://tailwindcss.com/docs/saturate
       */
      saturate: [{
        saturate: [Lt, ze, je]
      }],
      /**
       * Sepia
       * @see https://tailwindcss.com/docs/sepia
       */
      sepia: [{
        sepia: ["", Lt, ze, je]
      }],
      /**
       * Backdrop Filter
       * @see https://tailwindcss.com/docs/backdrop-filter
       */
      "backdrop-filter": [{
        "backdrop-filter": [
          // Deprecated since Tailwind CSS v3.0.0
          "",
          "none",
          ze,
          je
        ]
      }],
      /**
       * Backdrop Blur
       * @see https://tailwindcss.com/docs/backdrop-blur
       */
      "backdrop-blur": [{
        "backdrop-blur": St()
      }],
      /**
       * Backdrop Brightness
       * @see https://tailwindcss.com/docs/backdrop-brightness
       */
      "backdrop-brightness": [{
        "backdrop-brightness": [Lt, ze, je]
      }],
      /**
       * Backdrop Contrast
       * @see https://tailwindcss.com/docs/backdrop-contrast
       */
      "backdrop-contrast": [{
        "backdrop-contrast": [Lt, ze, je]
      }],
      /**
       * Backdrop Grayscale
       * @see https://tailwindcss.com/docs/backdrop-grayscale
       */
      "backdrop-grayscale": [{
        "backdrop-grayscale": ["", Lt, ze, je]
      }],
      /**
       * Backdrop Hue Rotate
       * @see https://tailwindcss.com/docs/backdrop-hue-rotate
       */
      "backdrop-hue-rotate": [{
        "backdrop-hue-rotate": [Lt, ze, je]
      }],
      /**
       * Backdrop Invert
       * @see https://tailwindcss.com/docs/backdrop-invert
       */
      "backdrop-invert": [{
        "backdrop-invert": ["", Lt, ze, je]
      }],
      /**
       * Backdrop Opacity
       * @see https://tailwindcss.com/docs/backdrop-opacity
       */
      "backdrop-opacity": [{
        "backdrop-opacity": [Lt, ze, je]
      }],
      /**
       * Backdrop Saturate
       * @see https://tailwindcss.com/docs/backdrop-saturate
       */
      "backdrop-saturate": [{
        "backdrop-saturate": [Lt, ze, je]
      }],
      /**
       * Backdrop Sepia
       * @see https://tailwindcss.com/docs/backdrop-sepia
       */
      "backdrop-sepia": [{
        "backdrop-sepia": ["", Lt, ze, je]
      }],
      // --------------
      // --- Tables ---
      // --------------
      /**
       * Border Collapse
       * @see https://tailwindcss.com/docs/border-collapse
       */
      "border-collapse": [{
        border: ["collapse", "separate"]
      }],
      /**
       * Border Spacing
       * @see https://tailwindcss.com/docs/border-spacing
       */
      "border-spacing": [{
        "border-spacing": be()
      }],
      /**
       * Border Spacing X
       * @see https://tailwindcss.com/docs/border-spacing
       */
      "border-spacing-x": [{
        "border-spacing-x": be()
      }],
      /**
       * Border Spacing Y
       * @see https://tailwindcss.com/docs/border-spacing
       */
      "border-spacing-y": [{
        "border-spacing-y": be()
      }],
      /**
       * Table Layout
       * @see https://tailwindcss.com/docs/table-layout
       */
      "table-layout": [{
        table: ["auto", "fixed"]
      }],
      /**
       * Caption Side
       * @see https://tailwindcss.com/docs/caption-side
       */
      caption: [{
        caption: ["top", "bottom"]
      }],
      // ---------------------------------
      // --- Transitions and Animation ---
      // ---------------------------------
      /**
       * Transition Property
       * @see https://tailwindcss.com/docs/transition-property
       */
      transition: [{
        transition: ["", "all", "colors", "opacity", "shadow", "transform", "none", ze, je]
      }],
      /**
       * Transition Behavior
       * @see https://tailwindcss.com/docs/transition-behavior
       */
      "transition-behavior": [{
        transition: ["normal", "discrete"]
      }],
      /**
       * Transition Duration
       * @see https://tailwindcss.com/docs/transition-duration
       */
      duration: [{
        duration: [Lt, "initial", ze, je]
      }],
      /**
       * Transition Timing Function
       * @see https://tailwindcss.com/docs/transition-timing-function
       */
      ease: [{
        ease: ["linear", "initial", Dt, ze, je]
      }],
      /**
       * Transition Delay
       * @see https://tailwindcss.com/docs/transition-delay
       */
      delay: [{
        delay: [Lt, ze, je]
      }],
      /**
       * Animation
       * @see https://tailwindcss.com/docs/animation
       */
      animate: [{
        animate: ["none", rt, ze, je]
      }],
      // ------------------
      // --- Transforms ---
      // ------------------
      /**
       * Backface Visibility
       * @see https://tailwindcss.com/docs/backface-visibility
       */
      backface: [{
        backface: ["hidden", "visible"]
      }],
      /**
       * Perspective
       * @see https://tailwindcss.com/docs/perspective
       */
      perspective: [{
        perspective: [de, ze, je]
      }],
      /**
       * Perspective Origin
       * @see https://tailwindcss.com/docs/perspective-origin
       */
      "perspective-origin": [{
        "perspective-origin": ke()
      }],
      /**
       * Rotate
       * @see https://tailwindcss.com/docs/rotate
       */
      rotate: [{
        rotate: ht()
      }],
      /**
       * Rotate X
       * @see https://tailwindcss.com/docs/rotate
       */
      "rotate-x": [{
        "rotate-x": ht()
      }],
      /**
       * Rotate Y
       * @see https://tailwindcss.com/docs/rotate
       */
      "rotate-y": [{
        "rotate-y": ht()
      }],
      /**
       * Rotate Z
       * @see https://tailwindcss.com/docs/rotate
       */
      "rotate-z": [{
        "rotate-z": ht()
      }],
      /**
       * Scale
       * @see https://tailwindcss.com/docs/scale
       */
      scale: [{
        scale: Wt()
      }],
      /**
       * Scale X
       * @see https://tailwindcss.com/docs/scale
       */
      "scale-x": [{
        "scale-x": Wt()
      }],
      /**
       * Scale Y
       * @see https://tailwindcss.com/docs/scale
       */
      "scale-y": [{
        "scale-y": Wt()
      }],
      /**
       * Scale Z
       * @see https://tailwindcss.com/docs/scale
       */
      "scale-z": [{
        "scale-z": Wt()
      }],
      /**
       * Scale 3D
       * @see https://tailwindcss.com/docs/scale
       */
      "scale-3d": ["scale-3d"],
      /**
       * Skew
       * @see https://tailwindcss.com/docs/skew
       */
      skew: [{
        skew: Fn()
      }],
      /**
       * Skew X
       * @see https://tailwindcss.com/docs/skew
       */
      "skew-x": [{
        "skew-x": Fn()
      }],
      /**
       * Skew Y
       * @see https://tailwindcss.com/docs/skew
       */
      "skew-y": [{
        "skew-y": Fn()
      }],
      /**
       * Transform
       * @see https://tailwindcss.com/docs/transform
       */
      transform: [{
        transform: [ze, je, "", "none", "gpu", "cpu"]
      }],
      /**
       * Transform Origin
       * @see https://tailwindcss.com/docs/transform-origin
       */
      "transform-origin": [{
        origin: ke()
      }],
      /**
       * Transform Style
       * @see https://tailwindcss.com/docs/transform-style
       */
      "transform-style": [{
        transform: ["3d", "flat"]
      }],
      /**
       * Translate
       * @see https://tailwindcss.com/docs/translate
       */
      translate: [{
        translate: Yn()
      }],
      /**
       * Translate X
       * @see https://tailwindcss.com/docs/translate
       */
      "translate-x": [{
        "translate-x": Yn()
      }],
      /**
       * Translate Y
       * @see https://tailwindcss.com/docs/translate
       */
      "translate-y": [{
        "translate-y": Yn()
      }],
      /**
       * Translate Z
       * @see https://tailwindcss.com/docs/translate
       */
      "translate-z": [{
        "translate-z": Yn()
      }],
      /**
       * Translate None
       * @see https://tailwindcss.com/docs/translate
       */
      "translate-none": ["translate-none"],
      // ---------------------
      // --- Interactivity ---
      // ---------------------
      /**
       * Accent Color
       * @see https://tailwindcss.com/docs/accent-color
       */
      accent: [{
        accent: I()
      }],
      /**
       * Appearance
       * @see https://tailwindcss.com/docs/appearance
       */
      appearance: [{
        appearance: ["none", "auto"]
      }],
      /**
       * Caret Color
       * @see https://tailwindcss.com/docs/just-in-time-mode#caret-color-utilities
       */
      "caret-color": [{
        caret: I()
      }],
      /**
       * Color Scheme
       * @see https://tailwindcss.com/docs/color-scheme
       */
      "color-scheme": [{
        scheme: ["normal", "dark", "light", "light-dark", "only-dark", "only-light"]
      }],
      /**
       * Cursor
       * @see https://tailwindcss.com/docs/cursor
       */
      cursor: [{
        cursor: ["auto", "default", "pointer", "wait", "text", "move", "help", "not-allowed", "none", "context-menu", "progress", "cell", "crosshair", "vertical-text", "alias", "copy", "no-drop", "grab", "grabbing", "all-scroll", "col-resize", "row-resize", "n-resize", "e-resize", "s-resize", "w-resize", "ne-resize", "nw-resize", "se-resize", "sw-resize", "ew-resize", "ns-resize", "nesw-resize", "nwse-resize", "zoom-in", "zoom-out", ze, je]
      }],
      /**
       * Field Sizing
       * @see https://tailwindcss.com/docs/field-sizing
       */
      "field-sizing": [{
        "field-sizing": ["fixed", "content"]
      }],
      /**
       * Pointer Events
       * @see https://tailwindcss.com/docs/pointer-events
       */
      "pointer-events": [{
        "pointer-events": ["auto", "none"]
      }],
      /**
       * Resize
       * @see https://tailwindcss.com/docs/resize
       */
      resize: [{
        resize: ["none", "", "y", "x"]
      }],
      /**
       * Scroll Behavior
       * @see https://tailwindcss.com/docs/scroll-behavior
       */
      "scroll-behavior": [{
        scroll: ["auto", "smooth"]
      }],
      /**
       * Scroll Margin
       * @see https://tailwindcss.com/docs/scroll-margin
       */
      "scroll-m": [{
        "scroll-m": be()
      }],
      /**
       * Scroll Margin X
       * @see https://tailwindcss.com/docs/scroll-margin
       */
      "scroll-mx": [{
        "scroll-mx": be()
      }],
      /**
       * Scroll Margin Y
       * @see https://tailwindcss.com/docs/scroll-margin
       */
      "scroll-my": [{
        "scroll-my": be()
      }],
      /**
       * Scroll Margin Start
       * @see https://tailwindcss.com/docs/scroll-margin
       */
      "scroll-ms": [{
        "scroll-ms": be()
      }],
      /**
       * Scroll Margin End
       * @see https://tailwindcss.com/docs/scroll-margin
       */
      "scroll-me": [{
        "scroll-me": be()
      }],
      /**
       * Scroll Margin Top
       * @see https://tailwindcss.com/docs/scroll-margin
       */
      "scroll-mt": [{
        "scroll-mt": be()
      }],
      /**
       * Scroll Margin Right
       * @see https://tailwindcss.com/docs/scroll-margin
       */
      "scroll-mr": [{
        "scroll-mr": be()
      }],
      /**
       * Scroll Margin Bottom
       * @see https://tailwindcss.com/docs/scroll-margin
       */
      "scroll-mb": [{
        "scroll-mb": be()
      }],
      /**
       * Scroll Margin Left
       * @see https://tailwindcss.com/docs/scroll-margin
       */
      "scroll-ml": [{
        "scroll-ml": be()
      }],
      /**
       * Scroll Padding
       * @see https://tailwindcss.com/docs/scroll-padding
       */
      "scroll-p": [{
        "scroll-p": be()
      }],
      /**
       * Scroll Padding X
       * @see https://tailwindcss.com/docs/scroll-padding
       */
      "scroll-px": [{
        "scroll-px": be()
      }],
      /**
       * Scroll Padding Y
       * @see https://tailwindcss.com/docs/scroll-padding
       */
      "scroll-py": [{
        "scroll-py": be()
      }],
      /**
       * Scroll Padding Start
       * @see https://tailwindcss.com/docs/scroll-padding
       */
      "scroll-ps": [{
        "scroll-ps": be()
      }],
      /**
       * Scroll Padding End
       * @see https://tailwindcss.com/docs/scroll-padding
       */
      "scroll-pe": [{
        "scroll-pe": be()
      }],
      /**
       * Scroll Padding Top
       * @see https://tailwindcss.com/docs/scroll-padding
       */
      "scroll-pt": [{
        "scroll-pt": be()
      }],
      /**
       * Scroll Padding Right
       * @see https://tailwindcss.com/docs/scroll-padding
       */
      "scroll-pr": [{
        "scroll-pr": be()
      }],
      /**
       * Scroll Padding Bottom
       * @see https://tailwindcss.com/docs/scroll-padding
       */
      "scroll-pb": [{
        "scroll-pb": be()
      }],
      /**
       * Scroll Padding Left
       * @see https://tailwindcss.com/docs/scroll-padding
       */
      "scroll-pl": [{
        "scroll-pl": be()
      }],
      /**
       * Scroll Snap Align
       * @see https://tailwindcss.com/docs/scroll-snap-align
       */
      "snap-align": [{
        snap: ["start", "end", "center", "align-none"]
      }],
      /**
       * Scroll Snap Stop
       * @see https://tailwindcss.com/docs/scroll-snap-stop
       */
      "snap-stop": [{
        snap: ["normal", "always"]
      }],
      /**
       * Scroll Snap Type
       * @see https://tailwindcss.com/docs/scroll-snap-type
       */
      "snap-type": [{
        snap: ["none", "x", "y", "both"]
      }],
      /**
       * Scroll Snap Type Strictness
       * @see https://tailwindcss.com/docs/scroll-snap-type
       */
      "snap-strictness": [{
        snap: ["mandatory", "proximity"]
      }],
      /**
       * Touch Action
       * @see https://tailwindcss.com/docs/touch-action
       */
      touch: [{
        touch: ["auto", "none", "manipulation"]
      }],
      /**
       * Touch Action X
       * @see https://tailwindcss.com/docs/touch-action
       */
      "touch-x": [{
        "touch-pan": ["x", "left", "right"]
      }],
      /**
       * Touch Action Y
       * @see https://tailwindcss.com/docs/touch-action
       */
      "touch-y": [{
        "touch-pan": ["y", "up", "down"]
      }],
      /**
       * Touch Action Pinch Zoom
       * @see https://tailwindcss.com/docs/touch-action
       */
      "touch-pz": ["touch-pinch-zoom"],
      /**
       * User Select
       * @see https://tailwindcss.com/docs/user-select
       */
      select: [{
        select: ["none", "text", "all", "auto"]
      }],
      /**
       * Will Change
       * @see https://tailwindcss.com/docs/will-change
       */
      "will-change": [{
        "will-change": ["auto", "scroll", "contents", "transform", ze, je]
      }],
      // -----------
      // --- SVG ---
      // -----------
      /**
       * Fill
       * @see https://tailwindcss.com/docs/fill
       */
      fill: [{
        fill: ["none", ...I()]
      }],
      /**
       * Stroke Width
       * @see https://tailwindcss.com/docs/stroke-width
       */
      "stroke-w": [{
        stroke: [Lt, dv, ic, US]
      }],
      /**
       * Stroke
       * @see https://tailwindcss.com/docs/stroke
       */
      stroke: [{
        stroke: ["none", ...I()]
      }],
      // ---------------------
      // --- Accessibility ---
      // ---------------------
      /**
       * Forced Color Adjust
       * @see https://tailwindcss.com/docs/forced-color-adjust
       */
      "forced-color-adjust": [{
        "forced-color-adjust": ["auto", "none"]
      }]
    },
    conflictingClassGroups: {
      overflow: ["overflow-x", "overflow-y"],
      overscroll: ["overscroll-x", "overscroll-y"],
      inset: ["inset-x", "inset-y", "start", "end", "top", "right", "bottom", "left"],
      "inset-x": ["right", "left"],
      "inset-y": ["top", "bottom"],
      flex: ["basis", "grow", "shrink"],
      gap: ["gap-x", "gap-y"],
      p: ["px", "py", "ps", "pe", "pt", "pr", "pb", "pl"],
      px: ["pr", "pl"],
      py: ["pt", "pb"],
      m: ["mx", "my", "ms", "me", "mt", "mr", "mb", "ml"],
      mx: ["mr", "ml"],
      my: ["mt", "mb"],
      size: ["w", "h"],
      "font-size": ["leading"],
      "fvn-normal": ["fvn-ordinal", "fvn-slashed-zero", "fvn-figure", "fvn-spacing", "fvn-fraction"],
      "fvn-ordinal": ["fvn-normal"],
      "fvn-slashed-zero": ["fvn-normal"],
      "fvn-figure": ["fvn-normal"],
      "fvn-spacing": ["fvn-normal"],
      "fvn-fraction": ["fvn-normal"],
      "line-clamp": ["display", "overflow"],
      rounded: ["rounded-s", "rounded-e", "rounded-t", "rounded-r", "rounded-b", "rounded-l", "rounded-ss", "rounded-se", "rounded-ee", "rounded-es", "rounded-tl", "rounded-tr", "rounded-br", "rounded-bl"],
      "rounded-s": ["rounded-ss", "rounded-es"],
      "rounded-e": ["rounded-se", "rounded-ee"],
      "rounded-t": ["rounded-tl", "rounded-tr"],
      "rounded-r": ["rounded-tr", "rounded-br"],
      "rounded-b": ["rounded-br", "rounded-bl"],
      "rounded-l": ["rounded-tl", "rounded-bl"],
      "border-spacing": ["border-spacing-x", "border-spacing-y"],
      "border-w": ["border-w-x", "border-w-y", "border-w-s", "border-w-e", "border-w-t", "border-w-r", "border-w-b", "border-w-l"],
      "border-w-x": ["border-w-r", "border-w-l"],
      "border-w-y": ["border-w-t", "border-w-b"],
      "border-color": ["border-color-x", "border-color-y", "border-color-s", "border-color-e", "border-color-t", "border-color-r", "border-color-b", "border-color-l"],
      "border-color-x": ["border-color-r", "border-color-l"],
      "border-color-y": ["border-color-t", "border-color-b"],
      translate: ["translate-x", "translate-y", "translate-none"],
      "translate-none": ["translate", "translate-x", "translate-y", "translate-z"],
      "scroll-m": ["scroll-mx", "scroll-my", "scroll-ms", "scroll-me", "scroll-mt", "scroll-mr", "scroll-mb", "scroll-ml"],
      "scroll-mx": ["scroll-mr", "scroll-ml"],
      "scroll-my": ["scroll-mt", "scroll-mb"],
      "scroll-p": ["scroll-px", "scroll-py", "scroll-ps", "scroll-pe", "scroll-pt", "scroll-pr", "scroll-pb", "scroll-pl"],
      "scroll-px": ["scroll-pr", "scroll-pl"],
      "scroll-py": ["scroll-pt", "scroll-pb"],
      touch: ["touch-x", "touch-y", "touch-pz"],
      "touch-x": ["touch"],
      "touch-y": ["touch"],
      "touch-pz": ["touch"]
    },
    conflictingClassGroupModifiers: {
      "font-size": ["leading"]
    },
    orderSensitiveModifiers: ["*", "**", "after", "backdrop", "before", "details-content", "file", "first-letter", "first-line", "marker", "placeholder", "selection"]
  };
}, ID = /* @__PURE__ */ ED($D);
function sc(...S) {
  return ID(nD(S));
}
const lc = wt.forwardRef(({ className: S, ...w }, b) => /* @__PURE__ */ C.jsx(
  "div",
  {
    ref: b,
    className: sc(
      "rounded-lg border bg-card text-card-foreground shadow-sm",
      S
    ),
    ...w
  }
));
lc.displayName = "Card";
const oc = wt.forwardRef(({ className: S, ...w }, b) => /* @__PURE__ */ C.jsx(
  "div",
  {
    ref: b,
    className: sc("flex flex-col space-y-1.5 p-6", S),
    ...w
  }
));
oc.displayName = "CardHeader";
const nd = wt.forwardRef(({ className: S, ...w }, b) => /* @__PURE__ */ C.jsx(
  "h3",
  {
    ref: b,
    className: sc(
      "text-2xl font-semibold leading-none tracking-tight",
      S
    ),
    ...w
  }
));
nd.displayName = "CardTitle";
const t1 = wt.forwardRef(({ className: S, ...w }, b) => /* @__PURE__ */ C.jsx(
  "p",
  {
    ref: b,
    className: sc("text-sm text-muted-foreground", S),
    ...w
  }
));
t1.displayName = "CardDescription";
const uc = wt.forwardRef(({ className: S, ...w }, b) => /* @__PURE__ */ C.jsx("div", { ref: b, className: sc("p-6 pt-0", S), ...w }));
uc.displayName = "CardContent";
const YD = wt.forwardRef(({ className: S, ...w }, b) => /* @__PURE__ */ C.jsx(
  "div",
  {
    ref: b,
    className: sc("flex items-center p-6 pt-0", S),
    ...w
  }
));
YD.displayName = "CardFooter";
const $S = wt.forwardRef(({ className: S, children: w, ...b }, U) => /* @__PURE__ */ C.jsx(
  "div",
  {
    ref: U,
    className: sc("relative overflow-hidden", S),
    ...b,
    children: /* @__PURE__ */ C.jsx("div", { className: "h-full w-full rounded-[inherit] overflow-auto", children: w })
  }
));
$S.displayName = "ScrollArea";
/**
 * @license lucide-react v0.563.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */
const n1 = (...S) => S.filter((w, b, U) => !!w && w.trim() !== "" && U.indexOf(w) === b).join(" ").trim();
/**
 * @license lucide-react v0.563.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */
const WD = (S) => S.replace(/([a-z0-9])([A-Z])/g, "$1-$2").toLowerCase();
/**
 * @license lucide-react v0.563.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */
const QD = (S) => S.replace(
  /^([A-Z])|[\s-_]+(\w)/g,
  (w, b, U) => U ? U.toUpperCase() : b.toLowerCase()
);
/**
 * @license lucide-react v0.563.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */
const HE = (S) => {
  const w = QD(S);
  return w.charAt(0).toUpperCase() + w.slice(1);
};
/**
 * @license lucide-react v0.563.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */
var GD = {
  xmlns: "http://www.w3.org/2000/svg",
  width: 24,
  height: 24,
  viewBox: "0 0 24 24",
  fill: "none",
  stroke: "currentColor",
  strokeWidth: 2,
  strokeLinecap: "round",
  strokeLinejoin: "round"
};
/**
 * @license lucide-react v0.563.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */
const qD = (S) => {
  for (const w in S)
    if (w.startsWith("aria-") || w === "role" || w === "title")
      return !0;
  return !1;
};
/**
 * @license lucide-react v0.563.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */
const XD = wt.forwardRef(
  ({
    color: S = "currentColor",
    size: w = 24,
    strokeWidth: b = 2,
    absoluteStrokeWidth: U,
    className: X = "",
    children: W,
    iconNode: y,
    ...ce
  }, B) => wt.createElement(
    "svg",
    {
      ref: B,
      ...GD,
      width: w,
      height: w,
      stroke: S,
      strokeWidth: U ? Number(b) * 24 / Number(w) : b,
      className: n1("lucide", X),
      ...!W && !qD(ce) && { "aria-hidden": "true" },
      ...ce
    },
    [
      ...y.map(([K, ye]) => wt.createElement(K, ye)),
      ...Array.isArray(W) ? W : [W]
    ]
  )
);
/**
 * @license lucide-react v0.563.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */
const Ho = (S, w) => {
  const b = wt.forwardRef(
    ({ className: U, ...X }, W) => wt.createElement(XD, {
      ref: W,
      iconNode: w,
      className: n1(
        `lucide-${WD(HE(S))}`,
        `lucide-${S}`,
        U
      ),
      ...X
    })
  );
  return b.displayName = HE(S), b;
};
/**
 * @license lucide-react v0.563.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */
const KD = [
  [
    "path",
    {
      d: "M22 12h-2.48a2 2 0 0 0-1.93 1.46l-2.35 8.36a.25.25 0 0 1-.48 0L9.24 2.18a.25.25 0 0 0-.48 0l-2.35 8.36A2 2 0 0 1 4.49 12H2",
      key: "169zse"
    }
  ]
], JD = Ho("activity", KD);
/**
 * @license lucide-react v0.563.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */
const ZD = [
  ["path", { d: "M12 18V5", key: "adv99a" }],
  ["path", { d: "M15 13a4.17 4.17 0 0 1-3-4 4.17 4.17 0 0 1-3 4", key: "1e3is1" }],
  ["path", { d: "M17.598 6.5A3 3 0 1 0 12 5a3 3 0 1 0-5.598 1.5", key: "1gqd8o" }],
  ["path", { d: "M17.997 5.125a4 4 0 0 1 2.526 5.77", key: "iwvgf7" }],
  ["path", { d: "M18 18a4 4 0 0 0 2-7.464", key: "efp6ie" }],
  ["path", { d: "M19.967 17.483A4 4 0 1 1 12 18a4 4 0 1 1-7.967-.517", key: "1gq6am" }],
  ["path", { d: "M6 18a4 4 0 0 1-2-7.464", key: "k1g0md" }],
  ["path", { d: "M6.003 5.125a4 4 0 0 0-2.526 5.77", key: "q97ue3" }]
], eN = Ho("brain", ZD);
/**
 * @license lucide-react v0.563.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */
const tN = [["path", { d: "m6 9 6 6 6-6", key: "qrunsl" }]], nN = Ho("chevron-down", tN);
/**
 * @license lucide-react v0.563.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */
const rN = [["path", { d: "m18 15-6-6-6 6", key: "153udz" }]], aN = Ho("chevron-up", rN);
/**
 * @license lucide-react v0.563.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */
const iN = [
  ["circle", { cx: "12", cy: "12", r: "10", key: "1mglay" }],
  ["path", { d: "M12 16v-4", key: "1dtifu" }],
  ["path", { d: "M12 8h.01", key: "e9boi3" }]
], lN = Ho("info", iN);
/**
 * @license lucide-react v0.563.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */
const oN = [["path", { d: "M21 12a9 9 0 1 1-6.219-8.56", key: "13zald" }]], sy = Ho("loader-circle", oN);
/**
 * @license lucide-react v0.563.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */
const uN = [
  [
    "path",
    {
      d: "M21.174 6.812a1 1 0 0 0-3.986-3.987L3.842 16.174a2 2 0 0 0-.5.83l-1.321 4.352a.5.5 0 0 0 .623.622l4.353-1.32a2 2 0 0 0 .83-.497z",
      key: "1a8usu"
    }
  ]
], sN = Ho("pen", uN);
/**
 * @license lucide-react v0.563.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */
const cN = [
  ["path", { d: "m21 21-4.34-4.34", key: "14j7rj" }],
  ["circle", { cx: "11", cy: "11", r: "8", key: "4ej97u" }]
], fN = Ho("search", cN);
/**
 * @license lucide-react v0.563.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */
const dN = [
  ["path", { d: "M21 5H3", key: "1fi0y6" }],
  ["path", { d: "M10 12H3", key: "1ulcyk" }],
  ["path", { d: "M10 19H3", key: "108z41" }],
  ["circle", { cx: "17", cy: "15", r: "3", key: "1upz2a" }],
  ["path", { d: "m21 19-1.9-1.9", key: "dwi7p8" }]
], pN = Ho("text-search", dN);
function vN({
  processedEvents: S,
  isLoading: w
}) {
  const [b, U] = wt.useState(!1), X = (W, y) => y === 0 && w && S.length === 0 ? /* @__PURE__ */ C.jsx(sy, { className: "h-4 w-4 text-neutral-400 animate-spin" }) : W.toLowerCase().includes("generating") ? /* @__PURE__ */ C.jsx(pN, { className: "h-4 w-4 text-neutral-400" }) : W.toLowerCase().includes("thinking") ? /* @__PURE__ */ C.jsx(sy, { className: "h-4 w-4 text-neutral-400 animate-spin" }) : W.toLowerCase().includes("reflection") ? /* @__PURE__ */ C.jsx(eN, { className: "h-4 w-4 text-neutral-400" }) : W.toLowerCase().includes("research") ? /* @__PURE__ */ C.jsx(fN, { className: "h-4 w-4 text-neutral-400" }) : W.toLowerCase().includes("finalizing") ? /* @__PURE__ */ C.jsx(sN, { className: "h-4 w-4 text-neutral-400" }) : /* @__PURE__ */ C.jsx(JD, { className: "h-4 w-4 text-neutral-400" });
  return wt.useEffect(() => {
    !w && S.length !== 0 && U(!0);
  }, [w, S]), /* @__PURE__ */ C.jsxs(lc, { className: "border-none rounded-lg bg-neutral-700 max-h-96", children: [
    /* @__PURE__ */ C.jsx(oc, { children: /* @__PURE__ */ C.jsx(t1, { className: "flex items-center justify-between", children: /* @__PURE__ */ C.jsxs(
      "div",
      {
        className: "flex items-center justify-start text-sm w-full cursor-pointer gap-2 text-neutral-100",
        onClick: () => U(!b),
        children: [
          "Research",
          b ? /* @__PURE__ */ C.jsx(nN, { className: "h-4 w-4 mr-2" }) : /* @__PURE__ */ C.jsx(aN, { className: "h-4 w-4 mr-2" })
        ]
      }
    ) }) }),
    !b && /* @__PURE__ */ C.jsx($S, { className: "max-h-96 overflow-y-auto", children: /* @__PURE__ */ C.jsxs(uc, { children: [
      w && S.length === 0 && /* @__PURE__ */ C.jsxs("div", { className: "relative pl-8 pb-4", children: [
        /* @__PURE__ */ C.jsx("div", { className: "absolute left-3 top-3.5 h-full w-0.5 bg-neutral-800" }),
        /* @__PURE__ */ C.jsx("div", { className: "absolute left-0.5 top-2 h-5 w-5 rounded-full bg-neutral-800 flex items-center justify-center ring-4 ring-neutral-900", children: /* @__PURE__ */ C.jsx(sy, { className: "h-3 w-3 text-neutral-400 animate-spin" }) }),
        /* @__PURE__ */ C.jsx("div", { children: /* @__PURE__ */ C.jsx("p", { className: "text-sm text-neutral-300 font-medium", children: "Searching..." }) })
      ] }),
      S.length > 0 ? /* @__PURE__ */ C.jsxs("div", { className: "space-y-0", children: [
        S.map((W, y) => /* @__PURE__ */ C.jsxs("div", { className: "relative pl-8 pb-4", children: [
          y < S.length - 1 || w && y === S.length - 1 ? /* @__PURE__ */ C.jsx("div", { className: "absolute left-3 top-3.5 h-full w-0.5 bg-neutral-600" }) : null,
          /* @__PURE__ */ C.jsx("div", { className: "absolute left-0.5 top-2 h-6 w-6 rounded-full bg-neutral-600 flex items-center justify-center ring-4 ring-neutral-700", children: X(W.title, y) }),
          /* @__PURE__ */ C.jsxs("div", { children: [
            /* @__PURE__ */ C.jsx("p", { className: "text-sm text-neutral-200 font-medium mb-0.5", children: W.title }),
            /* @__PURE__ */ C.jsx("p", { className: "text-xs text-neutral-300 leading-relaxed", children: typeof W.data == "string" ? W.data : Array.isArray(W.data) ? W.data.join(", ") : JSON.stringify(W.data) })
          ] })
        ] }, y)),
        w && S.length > 0 && /* @__PURE__ */ C.jsxs("div", { className: "relative pl-8 pb-4", children: [
          /* @__PURE__ */ C.jsx("div", { className: "absolute left-0.5 top-2 h-5 w-5 rounded-full bg-neutral-600 flex items-center justify-center ring-4 ring-neutral-700", children: /* @__PURE__ */ C.jsx(sy, { className: "h-3 w-3 text-neutral-400 animate-spin" }) }),
          /* @__PURE__ */ C.jsx("div", { children: /* @__PURE__ */ C.jsx("p", { className: "text-sm text-neutral-300 font-medium", children: "Searching..." }) })
        ] })
      ] }) : w ? null : (
        // Only show "No activity" if not loading and no events
        /* @__PURE__ */ C.jsxs("div", { className: "flex flex-col items-center justify-center h-full text-neutral-500 pt-10", children: [
          /* @__PURE__ */ C.jsx(lN, { className: "h-6 w-6 mb-3" }),
          /* @__PURE__ */ C.jsx("p", { className: "text-sm", children: "No activity to display." }),
          /* @__PURE__ */ C.jsx("p", { className: "text-xs text-neutral-600 mt-1", children: "Timeline will update during processing." })
        ] })
      )
    ] }) })
  ] });
}
function hN({
  queries: S,
  timeoutSeconds: w,
  researchTopic: b,
  onResponse: U
}) {
  const [X, W] = wt.useState(S), [y, ce] = wt.useState(null), [B, K] = wt.useState(!1), ye = (V) => {
    y === V ? (ce(null), K(!0)) : ce(V);
  }, ne = (V, $) => {
    const de = [...X];
    de[V] = $, W(de);
  }, oe = (V) => {
    U(V, V === "modify" ? { queries: X } : void 0);
  };
  return /* @__PURE__ */ C.jsxs("div", { className: "bg-neutral-700 rounded-lg border border-neutral-600 p-6 max-w-4xl mx-auto", children: [
    /* @__PURE__ */ C.jsxs("div", { className: "flex items-center gap-3 mb-6", children: [
      /* @__PURE__ */ C.jsx("div", { className: "text-2xl", children: "🔍" }),
      /* @__PURE__ */ C.jsxs("div", { children: [
        /* @__PURE__ */ C.jsx("h1", { className: "text-xl font-semibold text-neutral-100", children: "Query Approval Required" }),
        /* @__PURE__ */ C.jsx("p", { className: "text-sm text-neutral-400", children: "Review generated search queries" })
      ] })
    ] }),
    /* @__PURE__ */ C.jsxs("div", { className: "bg-neutral-600 p-4 rounded-md mb-6", children: [
      /* @__PURE__ */ C.jsx("strong", { className: "text-neutral-100", children: "Research Topic:" }),
      " ",
      b
    ] }),
    /* @__PURE__ */ C.jsxs("div", { className: "mb-6", children: [
      /* @__PURE__ */ C.jsxs("h3", { className: "text-lg font-medium text-neutral-100 mb-4", children: [
        "Generated Queries (",
        S.length,
        ")"
      ] }),
      /* @__PURE__ */ C.jsx("div", { className: "space-y-3 max-h-60 overflow-y-auto", children: S.map((V, $) => /* @__PURE__ */ C.jsx("div", { className: "bg-neutral-600 p-3 rounded-md border border-neutral-500", children: /* @__PURE__ */ C.jsxs("div", { className: "flex items-center gap-3", children: [
        /* @__PURE__ */ C.jsxs("span", { className: "text-sm font-mono text-neutral-300 min-w-[2rem]", children: [
          $ + 1,
          "."
        ] }),
        y === $ ? /* @__PURE__ */ C.jsx(
          "input",
          {
            type: "text",
            value: X[$],
            onChange: (de) => ne($, de.target.value),
            className: "flex-1 bg-neutral-500 text-neutral-100 px-3 py-1 rounded border border-neutral-400 focus:outline-none focus:border-blue-400",
            autoFocus: !0
          }
        ) : /* @__PURE__ */ C.jsx("span", { className: "flex-1 text-sm text-neutral-200", children: X[$] }),
        /* @__PURE__ */ C.jsx(
          "button",
          {
            onClick: () => ye($),
            className: "px-3 py-1 bg-neutral-500 hover:bg-neutral-400 text-neutral-100 rounded text-sm transition-colors",
            children: y === $ ? "💾 Save" : "✏️ Edit"
          }
        )
      ] }) }, $)) })
    ] }),
    w && /* @__PURE__ */ C.jsx("div", { className: "bg-yellow-900/20 border border-yellow-600/30 p-4 rounded-md mb-6", children: /* @__PURE__ */ C.jsxs("div", { className: "flex items-center gap-2 text-yellow-400", children: [
      /* @__PURE__ */ C.jsx("span", { children: "⏰" }),
      /* @__PURE__ */ C.jsxs("span", { children: [
        "This request will timeout in ",
        Math.floor(w / 60),
        " minutes"
      ] })
    ] }) }),
    /* @__PURE__ */ C.jsxs("div", { className: "flex gap-3 justify-end", children: [
      /* @__PURE__ */ C.jsx(
        "button",
        {
          onClick: () => oe("approve"),
          className: "px-6 py-3 bg-green-600 hover:bg-green-700 text-white rounded-md font-medium transition-colors",
          children: "✅ Approve All"
        }
      ),
      B && /* @__PURE__ */ C.jsx(
        "button",
        {
          onClick: () => oe("modify"),
          className: "px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-md font-medium transition-colors",
          children: "💾 Save Changes"
        }
      ),
      /* @__PURE__ */ C.jsx(
        "button",
        {
          onClick: () => oe("reject"),
          className: "px-6 py-3 bg-red-600 hover:bg-red-700 text-white rounded-md font-medium transition-colors",
          children: "❌ Reject & Stop"
        }
      )
    ] })
  ] });
}
function mN({
  papers: S,
  totalCount: w,
  recommendation: b,
  timeoutSeconds: U,
  onResponse: X
}) {
  const [W, y] = wt.useState(/* @__PURE__ */ new Set()), [ce, B] = wt.useState(""), K = wt.useMemo(() => {
    if (!ce.trim())
      return S;
    const $ = ce.toLowerCase();
    return S.filter(
      (de) => de.title.toLowerCase().includes($) || de.authors.some((Ae) => Ae.toLowerCase().includes($))
    );
  }, [S, ce]), ye = ($) => {
    const de = new Set(W);
    de.has($) ? de.delete($) : de.add($), y(de);
  }, ne = () => {
    W.size === K.length ? y(/* @__PURE__ */ new Set()) : y(new Set(K.map(($, de) => de)));
  }, oe = ($) => {
    if ($ === "select_subset") {
      const de = Array.from(W).map((Ae) => K[Ae]);
      X($, { selected_papers: de });
    } else
      X($);
  }, V = ($) => $.length <= 2 ? $.join(", ") : `${$.slice(0, 2).join(", ")} et al.`;
  return /* @__PURE__ */ C.jsxs("div", { className: "bg-neutral-700 rounded-lg border border-neutral-600 p-6 max-w-6xl mx-auto", children: [
    /* @__PURE__ */ C.jsxs("div", { className: "flex items-center gap-3 mb-6", children: [
      /* @__PURE__ */ C.jsx("div", { className: "text-2xl", children: "📄" }),
      /* @__PURE__ */ C.jsxs("div", { children: [
        /* @__PURE__ */ C.jsx("h1", { className: "text-xl font-semibold text-neutral-100", children: "Paper Selection Required" }),
        /* @__PURE__ */ C.jsxs("p", { className: "text-sm text-neutral-400", children: [
          "Found ",
          w,
          " papers - select papers to analyze"
        ] })
      ] })
    ] }),
    /* @__PURE__ */ C.jsxs("div", { className: "bg-neutral-600 p-4 rounded-md mb-6", children: [
      "💡 ",
      /* @__PURE__ */ C.jsx("strong", { className: "text-neutral-100", children: "Recommendation:" }),
      " ",
      b || "Select 10-20 most relevant papers for detailed analysis"
    ] }),
    /* @__PURE__ */ C.jsx("div", { className: "flex items-center justify-between mb-4", children: /* @__PURE__ */ C.jsxs("div", { className: "flex items-center gap-4", children: [
      /* @__PURE__ */ C.jsxs("span", { className: "text-sm text-neutral-300", children: [
        W.size,
        " / ",
        K.length,
        " papers selected"
      ] }),
      /* @__PURE__ */ C.jsx("div", { className: "flex gap-2", children: /* @__PURE__ */ C.jsx(
        "button",
        {
          onClick: ne,
          className: "px-3 py-1 bg-neutral-600 hover:bg-neutral-500 text-neutral-100 rounded text-sm transition-colors",
          children: W.size === K.length ? "Clear All" : "Select All"
        }
      ) })
    ] }) }),
    K.length > 5 && /* @__PURE__ */ C.jsx("div", { className: "mb-4", children: /* @__PURE__ */ C.jsx(
      "input",
      {
        type: "text",
        placeholder: "🔍 Filter papers by title or author...",
        value: ce,
        onChange: ($) => B($.target.value),
        className: "w-full px-3 py-2 bg-neutral-600 text-neutral-100 rounded border border-neutral-500 focus:outline-none focus:border-blue-400"
      }
    ) }),
    /* @__PURE__ */ C.jsx("div", { className: "max-h-96 overflow-y-auto mb-6 space-y-3", children: K.map(($, de) => {
      const Ae = S.indexOf($), Dt = W.has(de);
      return /* @__PURE__ */ C.jsx(
        "div",
        {
          className: `border rounded-md p-4 cursor-pointer transition-colors ${Dt ? "border-blue-400 bg-blue-900/20" : "border-neutral-500 bg-neutral-600 hover:border-neutral-400"}`,
          onClick: () => ye(de),
          children: /* @__PURE__ */ C.jsxs("div", { className: "flex items-start gap-3", children: [
            /* @__PURE__ */ C.jsx(
              "input",
              {
                type: "checkbox",
                checked: Dt,
                onChange: () => ye(de),
                className: "mt-1 w-4 h-4 text-blue-600 bg-neutral-600 border-neutral-500 rounded focus:ring-blue-500",
                onClick: (rt) => rt.stopPropagation()
              }
            ),
            /* @__PURE__ */ C.jsxs("div", { className: "flex-1", children: [
              /* @__PURE__ */ C.jsxs("h4", { className: "text-sm font-medium text-neutral-100 mb-1", children: [
                "[",
                de + 1,
                "] ",
                $.title
              ] }),
              /* @__PURE__ */ C.jsxs("div", { className: "text-xs text-neutral-400 mb-2", children: [
                V($.authors),
                $.year && ` (${$.year})`
              ] }),
              /* @__PURE__ */ C.jsxs("div", { className: "flex gap-4 text-xs text-neutral-500 mb-2", children: [
                $.doi && /* @__PURE__ */ C.jsxs("span", { children: [
                  "DOI: ",
                  /* @__PURE__ */ C.jsx("span", { className: "text-blue-400", children: $.doi })
                ] }),
                $.arxiv_id && /* @__PURE__ */ C.jsxs("span", { children: [
                  "arXiv: ",
                  /* @__PURE__ */ C.jsx("span", { className: "text-blue-400", children: $.arxiv_id })
                ] })
              ] }),
              $.abstract && /* @__PURE__ */ C.jsx("div", { className: "text-xs text-neutral-300 line-clamp-3", children: $.abstract.length > 200 ? `${$.abstract.substring(0, 200)}...` : $.abstract })
            ] })
          ] })
        },
        Ae
      );
    }) }),
    U && /* @__PURE__ */ C.jsx("div", { className: "bg-yellow-900/20 border border-yellow-600/30 p-4 rounded-md mb-6", children: /* @__PURE__ */ C.jsxs("div", { className: "flex items-center gap-2 text-yellow-400", children: [
      /* @__PURE__ */ C.jsx("span", { children: "⏰" }),
      /* @__PURE__ */ C.jsxs("span", { children: [
        "This request will timeout in ",
        Math.floor(U / 60),
        " minutes"
      ] })
    ] }) }),
    /* @__PURE__ */ C.jsxs("div", { className: "flex gap-3 justify-end", children: [
      /* @__PURE__ */ C.jsxs(
        "button",
        {
          onClick: () => oe("select_subset"),
          disabled: W.size === 0,
          className: "px-6 py-3 bg-green-600 hover:bg-green-700 disabled:bg-neutral-600 disabled:cursor-not-allowed text-white rounded-md font-medium transition-colors",
          children: [
            "✅ Submit Selection (",
            W.size,
            ")"
          ]
        }
      ),
      /* @__PURE__ */ C.jsx(
        "button",
        {
          onClick: () => oe("select_all"),
          className: "px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-md font-medium transition-colors",
          children: "📚 Analyze All Papers"
        }
      ),
      /* @__PURE__ */ C.jsx(
        "button",
        {
          onClick: () => oe("reject"),
          className: "px-6 py-3 bg-red-600 hover:bg-red-700 text-white rounded-md font-medium transition-colors",
          children: "❌ Cancel Research"
        }
      )
    ] })
  ] });
}
function yN({
  report: S,
  wordCount: w,
  paperCount: b,
  researchTopic: U,
  timeoutSeconds: X,
  onResponse: W
}) {
  const [y, ce] = wt.useState(!1), [B, K] = wt.useState(""), ye = (V) => {
    if (V === "modify") {
      if (!B.trim()) {
        alert("Please provide feedback before submitting modifications");
        return;
      }
      W(V, { feedback: B.trim() });
    } else
      W(V);
  }, ne = () => {
    y ? ye("modify") : ce(!0);
  }, oe = () => {
    navigator.clipboard.writeText(S);
  };
  return /* @__PURE__ */ C.jsxs("div", { className: "bg-neutral-700 rounded-lg border border-neutral-600 p-6 max-w-6xl mx-auto", children: [
    /* @__PURE__ */ C.jsxs("div", { className: "flex items-center gap-3 mb-6", children: [
      /* @__PURE__ */ C.jsx("div", { className: "text-2xl", children: "📝" }),
      /* @__PURE__ */ C.jsxs("div", { children: [
        /* @__PURE__ */ C.jsx("h1", { className: "text-xl font-semibold text-neutral-100", children: "Report Review Required" }),
        /* @__PURE__ */ C.jsx("p", { className: "text-sm text-neutral-400", children: "Review and approve the research report" })
      ] })
    ] }),
    /* @__PURE__ */ C.jsxs("div", { className: "bg-neutral-600 p-4 rounded-md mb-6", children: [
      /* @__PURE__ */ C.jsx("strong", { className: "text-neutral-100", children: "Research Topic:" }),
      " ",
      U
    ] }),
    /* @__PURE__ */ C.jsxs("div", { className: "grid grid-cols-2 gap-4 mb-6", children: [
      /* @__PURE__ */ C.jsxs("div", { className: "bg-neutral-600 p-4 rounded-md", children: [
        /* @__PURE__ */ C.jsx("div", { className: "text-sm text-neutral-400", children: "Word Count" }),
        /* @__PURE__ */ C.jsx("div", { className: "text-xl font-bold text-neutral-100", children: w.toLocaleString() })
      ] }),
      /* @__PURE__ */ C.jsxs("div", { className: "bg-neutral-600 p-4 rounded-md", children: [
        /* @__PURE__ */ C.jsx("div", { className: "text-sm text-neutral-400", children: "Papers Analyzed" }),
        /* @__PURE__ */ C.jsx("div", { className: "text-xl font-bold text-neutral-100", children: b })
      ] })
    ] }),
    /* @__PURE__ */ C.jsxs("div", { className: "mb-6", children: [
      /* @__PURE__ */ C.jsx("h3", { className: "text-lg font-medium text-neutral-100 mb-4", children: "Generated Report" }),
      /* @__PURE__ */ C.jsx("div", { className: "bg-neutral-600 border border-neutral-500 rounded-md p-4 max-h-96 overflow-y-auto", children: /* @__PURE__ */ C.jsx("pre", { className: "text-sm text-neutral-200 whitespace-pre-wrap font-sans", children: S }) })
    ] }),
    y && /* @__PURE__ */ C.jsxs("div", { className: "mb-6", children: [
      /* @__PURE__ */ C.jsx("h3", { className: "text-lg font-medium text-neutral-100 mb-4", children: "Modification Feedback" }),
      /* @__PURE__ */ C.jsx(
        "textarea",
        {
          value: B,
          onChange: (V) => K(V.target.value),
          placeholder: `Please provide specific feedback on what should be changed...

Examples:
- Add more details about methodology
- Focus more on recent papers (2023-2024)
- Include more quantitative results
- Expand the conclusion section`,
          className: "w-full h-32 px-3 py-2 bg-neutral-600 text-neutral-100 rounded border border-neutral-500 focus:outline-none focus:border-blue-400 resize-none",
          autoFocus: !0
        }
      )
    ] }),
    X && /* @__PURE__ */ C.jsx("div", { className: "bg-yellow-900/20 border border-yellow-600/30 p-4 rounded-md mb-6", children: /* @__PURE__ */ C.jsxs("div", { className: "flex items-center gap-2 text-yellow-400", children: [
      /* @__PURE__ */ C.jsx("span", { children: "⏰" }),
      /* @__PURE__ */ C.jsxs("span", { children: [
        "This request will timeout in ",
        Math.floor(X / 60),
        " minutes"
      ] })
    ] }) }),
    /* @__PURE__ */ C.jsxs("div", { className: "flex gap-3 justify-end", children: [
      /* @__PURE__ */ C.jsx(
        "button",
        {
          onClick: () => ye("approve"),
          className: "px-6 py-3 bg-green-600 hover:bg-green-700 text-white rounded-md font-medium transition-colors",
          children: "✅ Approve Report"
        }
      ),
      /* @__PURE__ */ C.jsx(
        "button",
        {
          onClick: ne,
          className: "px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-md font-medium transition-colors",
          children: y ? "💾 Submit Feedback" : "✏️ Request Modifications"
        }
      ),
      /* @__PURE__ */ C.jsx(
        "button",
        {
          onClick: oe,
          className: "px-6 py-3 bg-neutral-600 hover:bg-neutral-500 text-neutral-100 rounded-md font-medium transition-colors",
          children: "📋 Copy to Clipboard"
        }
      ),
      /* @__PURE__ */ C.jsx(
        "button",
        {
          onClick: () => ye("reject"),
          className: "px-6 py-3 bg-red-600 hover:bg-red-700 text-white rounded-md font-medium transition-colors",
          children: "❌ Reject & Stop"
        }
      )
    ] })
  ] });
}
function gN({ onSelectSession: S, onCreateNewSession: w }) {
  const [b, U] = wt.useState([]), [X, W] = wt.useState(!0), [y, ce] = wt.useState("all"), [B, K] = wt.useState("");
  wt.useEffect(() => {
    ye();
  }, []);
  const ye = async () => {
    W(!0);
    try {
      const $ = [
        {
          id: "session-1",
          thread_id: "thread-1",
          title: "AI in Healthcare Research",
          research_topic: "Applications of artificial intelligence in healthcare",
          created_at: (/* @__PURE__ */ new Date()).toISOString(),
          updated_at: (/* @__PURE__ */ new Date()).toISOString(),
          status: "completed",
          paper_count: 15,
          report_count: 1,
          tags: ["healthcare", "ai"]
        },
        {
          id: "session-2",
          thread_id: "thread-2",
          title: "Machine Learning Algorithms",
          research_topic: "Latest advances in machine learning algorithms",
          created_at: new Date(Date.now() - 864e5).toISOString(),
          updated_at: new Date(Date.now() - 864e5).toISOString(),
          status: "in_progress",
          paper_count: 8,
          report_count: 0,
          tags: ["ml", "algorithms"]
        }
      ];
      U($);
    } catch ($) {
      console.error("Failed to load sessions:", $);
    } finally {
      W(!1);
    }
  }, ne = ($) => {
    switch ($) {
      case "completed":
        return "✅";
      case "in_progress":
        return "🔄";
      case "paused":
        return "⏸️";
      case "failed":
        return "❌";
      default:
        return "❓";
    }
  }, oe = b.filter(($) => {
    const de = y === "all" || $.status === y, Ae = !B || $.title.toLowerCase().includes(B.toLowerCase()) || $.research_topic.toLowerCase().includes(B.toLowerCase());
    return de && Ae;
  }), V = ($) => new Date($).toLocaleDateString();
  return X ? /* @__PURE__ */ C.jsx("div", { className: "p-6", children: /* @__PURE__ */ C.jsx("div", { className: "animate-pulse space-y-4", children: [...Array(3)].map(($, de) => /* @__PURE__ */ C.jsx("div", { className: "bg-neutral-700 h-24 rounded-lg" }, de)) }) }) : /* @__PURE__ */ C.jsxs("div", { className: "p-6", children: [
    /* @__PURE__ */ C.jsxs("div", { className: "flex items-center justify-between mb-6", children: [
      /* @__PURE__ */ C.jsx("h2", { className: "text-xl font-semibold text-neutral-100", children: "Research Sessions" }),
      /* @__PURE__ */ C.jsx(
        "button",
        {
          onClick: w,
          className: "px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-md font-medium transition-colors",
          children: "+ New Session"
        }
      )
    ] }),
    /* @__PURE__ */ C.jsxs("div", { className: "mb-4 space-y-3", children: [
      /* @__PURE__ */ C.jsx(
        "input",
        {
          type: "text",
          placeholder: "Search sessions...",
          value: B,
          onChange: ($) => K($.target.value),
          className: "w-full px-3 py-2 bg-neutral-700 text-neutral-100 rounded border border-neutral-600 focus:outline-none focus:border-blue-400"
        }
      ),
      /* @__PURE__ */ C.jsx("div", { className: "flex gap-2", children: ["all", "completed", "in_progress", "failed"].map(($) => /* @__PURE__ */ C.jsx(
        "button",
        {
          onClick: () => ce($),
          className: `px-3 py-1 rounded text-sm font-medium transition-colors ${y === $ ? "bg-blue-600 text-white" : "bg-neutral-700 text-neutral-300 hover:bg-neutral-600"}`,
          children: $ === "all" ? "All" : $ === "completed" ? "Completed" : $ === "in_progress" ? "In Progress" : "Failed"
        },
        $
      )) })
    ] }),
    /* @__PURE__ */ C.jsx("div", { className: "space-y-3", children: oe.length === 0 ? /* @__PURE__ */ C.jsxs("div", { className: "text-center py-8 text-neutral-400", children: [
      /* @__PURE__ */ C.jsx("div", { className: "text-4xl mb-4", children: "📚" }),
      /* @__PURE__ */ C.jsx("p", { children: "No sessions found" }),
      /* @__PURE__ */ C.jsx("p", { className: "text-sm", children: "Try adjusting your search or filters" })
    ] }) : oe.map(($) => /* @__PURE__ */ C.jsx(
      "div",
      {
        onClick: () => S($.id),
        className: "bg-neutral-700 border border-neutral-600 rounded-lg p-4 cursor-pointer hover:border-neutral-500 transition-colors",
        children: /* @__PURE__ */ C.jsx("div", { className: "flex items-start justify-between", children: /* @__PURE__ */ C.jsxs("div", { className: "flex-1", children: [
          /* @__PURE__ */ C.jsxs("div", { className: "flex items-center gap-2 mb-2", children: [
            /* @__PURE__ */ C.jsx("span", { className: "text-lg", children: ne($.status) }),
            /* @__PURE__ */ C.jsx("h3", { className: "font-medium text-neutral-100", children: $.title })
          ] }),
          /* @__PURE__ */ C.jsx("p", { className: "text-sm text-neutral-300 mb-3 line-clamp-2", children: $.research_topic }),
          /* @__PURE__ */ C.jsxs("div", { className: "flex items-center gap-4 text-xs text-neutral-400", children: [
            /* @__PURE__ */ C.jsxs("span", { children: [
              "📄 ",
              $.paper_count,
              " papers"
            ] }),
            /* @__PURE__ */ C.jsxs("span", { children: [
              "📝 ",
              $.report_count,
              " reports"
            ] }),
            /* @__PURE__ */ C.jsxs("span", { children: [
              "📅 ",
              V($.updated_at)
            ] })
          ] }),
          $.tags.length > 0 && /* @__PURE__ */ C.jsx("div", { className: "flex gap-2 mt-3", children: $.tags.slice(0, 3).map((de) => /* @__PURE__ */ C.jsx(
            "span",
            {
              className: "px-2 py-1 bg-neutral-600 text-neutral-300 text-xs rounded",
              children: de
            },
            de
          )) })
        ] }) })
      },
      $.id
    )) })
  ] });
}
function SN({ sessionId: S, onBack: w, onOpenPaper: b, onExportReport: U }) {
  const [X, W] = wt.useState(null), [y, ce] = wt.useState(!0), [B, K] = wt.useState("overview");
  wt.useEffect(() => {
    ye();
  }, [S]);
  const ye = async () => {
    ce(!0);
    try {
      const V = {
        id: S,
        title: "AI in Healthcare Research",
        research_topic: "Applications of artificial intelligence in healthcare diagnostics and treatment",
        created_at: (/* @__PURE__ */ new Date()).toISOString(),
        updated_at: (/* @__PURE__ */ new Date()).toISOString(),
        status: "completed",
        papers: [
          {
            id: "paper-1",
            title: "Deep Learning for Medical Image Analysis",
            authors: ["Smith, J.", "Johnson, A.", "Williams, R."],
            year: 2023,
            doi: "10.1038/s41591-023-01234-5",
            abstract: "This paper presents a comprehensive review of deep learning applications in medical imaging..."
          },
          {
            id: "paper-2",
            title: "AI-Driven Drug Discovery: Current Trends and Future Directions",
            authors: ["Brown, M.", "Davis, L."],
            year: 2024,
            arxiv_id: "2401.12345",
            abstract: "Recent advances in artificial intelligence have revolutionized drug discovery processes..."
          }
        ],
        reports: [
          {
            id: "report-1",
            title: "Comprehensive Analysis of AI in Healthcare",
            content: `# AI in Healthcare: Current State and Future Prospects

## Executive Summary

Artificial intelligence is transforming healthcare delivery...`,
            word_count: 2450,
            created_at: (/* @__PURE__ */ new Date()).toISOString()
          }
        ],
        query_count: 15,
        total_tokens: 125e3,
        execution_time: 1800
        // seconds
      };
      W(V);
    } catch (V) {
      console.error("Failed to load session detail:", V);
    } finally {
      ce(!1);
    }
  }, ne = (V) => new Date(V).toLocaleString(), oe = (V) => {
    const $ = Math.floor(V / 3600), de = Math.floor(V % 3600 / 60);
    return $ > 0 ? `${$}h ${de}m` : `${de}m`;
  };
  return y ? /* @__PURE__ */ C.jsx("div", { className: "p-6", children: /* @__PURE__ */ C.jsxs("div", { className: "animate-pulse space-y-6", children: [
    /* @__PURE__ */ C.jsx("div", { className: "h-8 bg-neutral-700 rounded w-1/4" }),
    /* @__PURE__ */ C.jsx("div", { className: "h-64 bg-neutral-700 rounded" })
  ] }) }) : X ? /* @__PURE__ */ C.jsxs("div", { className: "p-6", children: [
    /* @__PURE__ */ C.jsxs("div", { className: "flex items-center gap-4 mb-6", children: [
      /* @__PURE__ */ C.jsx(
        "button",
        {
          onClick: w,
          className: "px-3 py-1 bg-neutral-700 hover:bg-neutral-600 text-neutral-300 rounded transition-colors",
          children: "← Back"
        }
      ),
      /* @__PURE__ */ C.jsxs("div", { children: [
        /* @__PURE__ */ C.jsx("h1", { className: "text-2xl font-bold text-neutral-100", children: X.title }),
        /* @__PURE__ */ C.jsx("p", { className: "text-sm text-neutral-400", children: X.research_topic })
      ] })
    ] }),
    /* @__PURE__ */ C.jsx("div", { className: "flex gap-1 mb-6 border-b border-neutral-700", children: [
      { key: "overview", label: "Overview", icon: "📊" },
      { key: "papers", label: "Papers", icon: "📄", count: X.papers.length },
      { key: "reports", label: "Reports", icon: "📝", count: X.reports.length }
    ].map((V) => /* @__PURE__ */ C.jsxs(
      "button",
      {
        onClick: () => K(V.key),
        className: `px-4 py-2 rounded-t-md font-medium transition-colors ${B === V.key ? "bg-neutral-700 text-neutral-100 border-b-2 border-blue-400" : "text-neutral-400 hover:text-neutral-300"}`,
        children: [
          V.icon,
          " ",
          V.label,
          " ",
          V.count !== void 0 && `(${V.count})`
        ]
      },
      V.key
    )) }),
    /* @__PURE__ */ C.jsxs("div", { className: "space-y-6", children: [
      B === "overview" && /* @__PURE__ */ C.jsxs("div", { className: "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6", children: [
        /* @__PURE__ */ C.jsxs(lc, { className: "bg-neutral-700 border-neutral-600", children: [
          /* @__PURE__ */ C.jsx(oc, { children: /* @__PURE__ */ C.jsx(nd, { className: "text-neutral-100 flex items-center gap-2", children: "📊 Statistics" }) }),
          /* @__PURE__ */ C.jsxs(uc, { className: "space-y-3", children: [
            /* @__PURE__ */ C.jsxs("div", { className: "flex justify-between", children: [
              /* @__PURE__ */ C.jsx("span", { className: "text-neutral-400", children: "Papers Found:" }),
              /* @__PURE__ */ C.jsx("span", { className: "text-neutral-100 font-medium", children: X.papers.length })
            ] }),
            /* @__PURE__ */ C.jsxs("div", { className: "flex justify-between", children: [
              /* @__PURE__ */ C.jsx("span", { className: "text-neutral-400", children: "Queries Executed:" }),
              /* @__PURE__ */ C.jsx("span", { className: "text-neutral-100 font-medium", children: X.query_count })
            ] }),
            /* @__PURE__ */ C.jsxs("div", { className: "flex justify-between", children: [
              /* @__PURE__ */ C.jsx("span", { className: "text-neutral-400", children: "Total Tokens:" }),
              /* @__PURE__ */ C.jsx("span", { className: "text-neutral-100 font-medium", children: X.total_tokens.toLocaleString() })
            ] }),
            /* @__PURE__ */ C.jsxs("div", { className: "flex justify-between", children: [
              /* @__PURE__ */ C.jsx("span", { className: "text-neutral-400", children: "Execution Time:" }),
              /* @__PURE__ */ C.jsx("span", { className: "text-neutral-100 font-medium", children: oe(X.execution_time) })
            ] })
          ] })
        ] }),
        /* @__PURE__ */ C.jsxs(lc, { className: "bg-neutral-700 border-neutral-600", children: [
          /* @__PURE__ */ C.jsx(oc, { children: /* @__PURE__ */ C.jsx(nd, { className: "text-neutral-100 flex items-center gap-2", children: "📅 Timeline" }) }),
          /* @__PURE__ */ C.jsxs(uc, { className: "space-y-3", children: [
            /* @__PURE__ */ C.jsxs("div", { className: "flex justify-between", children: [
              /* @__PURE__ */ C.jsx("span", { className: "text-neutral-400", children: "Created:" }),
              /* @__PURE__ */ C.jsx("span", { className: "text-neutral-100 font-medium text-sm", children: ne(X.created_at) })
            ] }),
            /* @__PURE__ */ C.jsxs("div", { className: "flex justify-between", children: [
              /* @__PURE__ */ C.jsx("span", { className: "text-neutral-400", children: "Last Updated:" }),
              /* @__PURE__ */ C.jsx("span", { className: "text-neutral-100 font-medium text-sm", children: ne(X.updated_at) })
            ] }),
            /* @__PURE__ */ C.jsxs("div", { className: "flex justify-between", children: [
              /* @__PURE__ */ C.jsx("span", { className: "text-neutral-400", children: "Status:" }),
              /* @__PURE__ */ C.jsx("span", { className: `font-medium ${X.status === "completed" ? "text-green-400" : X.status === "in_progress" ? "text-blue-400" : X.status === "failed" ? "text-red-400" : "text-yellow-400"}`, children: X.status.replace("_", " ").toUpperCase() })
            ] })
          ] })
        ] }),
        /* @__PURE__ */ C.jsxs(lc, { className: "bg-neutral-700 border-neutral-600", children: [
          /* @__PURE__ */ C.jsx(oc, { children: /* @__PURE__ */ C.jsx(nd, { className: "text-neutral-100 flex items-center gap-2", children: "📈 Summary" }) }),
          /* @__PURE__ */ C.jsx(uc, { children: /* @__PURE__ */ C.jsxs("p", { className: "text-neutral-300 text-sm leading-relaxed", children: [
            "This research session explored ",
            X.research_topic,
            ". Found ",
            X.papers.length,
            " relevant papers and generated ",
            X.reports.length,
            " comprehensive reports."
          ] }) })
        ] })
      ] }),
      B === "papers" && /* @__PURE__ */ C.jsx("div", { className: "space-y-4", children: X.papers.map((V) => /* @__PURE__ */ C.jsxs(lc, { className: "bg-neutral-700 border-neutral-600", children: [
        /* @__PURE__ */ C.jsx(oc, { children: /* @__PURE__ */ C.jsxs("div", { className: "flex items-start justify-between", children: [
          /* @__PURE__ */ C.jsxs("div", { className: "flex-1", children: [
            /* @__PURE__ */ C.jsx(nd, { className: "text-neutral-100 text-lg", children: V.title }),
            /* @__PURE__ */ C.jsxs("p", { className: "text-neutral-400 text-sm mt-1", children: [
              V.authors.join(", "),
              " ",
              V.year && `(${V.year})`
            ] })
          ] }),
          /* @__PURE__ */ C.jsx(
            "button",
            {
              onClick: () => b(X.id, V.id),
              className: "px-3 py-1 bg-blue-600 hover:bg-blue-700 text-white text-sm rounded transition-colors",
              children: "📖 Open"
            }
          )
        ] }) }),
        /* @__PURE__ */ C.jsxs(uc, { children: [
          /* @__PURE__ */ C.jsxs("div", { className: "flex gap-4 text-xs text-neutral-400 mb-3", children: [
            V.doi && /* @__PURE__ */ C.jsxs("span", { children: [
              "DOI: ",
              V.doi
            ] }),
            V.arxiv_id && /* @__PURE__ */ C.jsxs("span", { children: [
              "arXiv: ",
              V.arxiv_id
            ] })
          ] }),
          V.abstract && /* @__PURE__ */ C.jsx("p", { className: "text-neutral-300 text-sm leading-relaxed", children: V.abstract.length > 300 ? `${V.abstract.substring(0, 300)}...` : V.abstract })
        ] })
      ] }, V.id)) }),
      B === "reports" && /* @__PURE__ */ C.jsx("div", { className: "space-y-4", children: X.reports.map((V) => /* @__PURE__ */ C.jsxs(lc, { className: "bg-neutral-700 border-neutral-600", children: [
        /* @__PURE__ */ C.jsx(oc, { children: /* @__PURE__ */ C.jsxs("div", { className: "flex items-start justify-between", children: [
          /* @__PURE__ */ C.jsxs("div", { className: "flex-1", children: [
            /* @__PURE__ */ C.jsx(nd, { className: "text-neutral-100 text-lg", children: V.title }),
            /* @__PURE__ */ C.jsxs("p", { className: "text-neutral-400 text-sm mt-1", children: [
              ne(V.created_at),
              " • ",
              V.word_count.toLocaleString(),
              " words"
            ] })
          ] }),
          /* @__PURE__ */ C.jsx(
            "button",
            {
              onClick: () => U(X.id, V.id),
              className: "px-3 py-1 bg-green-600 hover:bg-green-700 text-white text-sm rounded transition-colors",
              children: "💾 Export"
            }
          )
        ] }) }),
        /* @__PURE__ */ C.jsx(uc, { children: /* @__PURE__ */ C.jsx($S, { className: "max-h-64", children: /* @__PURE__ */ C.jsx("pre", { className: "text-neutral-300 text-sm whitespace-pre-wrap font-sans", children: V.content.length > 1e3 ? `${V.content.substring(0, 1e3)}...` : V.content }) }) })
      ] }, V.id)) })
    ] })
  ] }) : /* @__PURE__ */ C.jsxs("div", { className: "p-6 text-center", children: [
    /* @__PURE__ */ C.jsx("p", { className: "text-neutral-400", children: "Failed to load session details" }),
    /* @__PURE__ */ C.jsx(
      "button",
      {
        onClick: w,
        className: "mt-4 px-4 py-2 bg-neutral-600 hover:bg-neutral-500 text-neutral-100 rounded transition-colors",
        children: "← Back to Sessions"
      }
    )
  ] });
}
const pv = window.acquireVsCodeApi(), xN = () => {
  const [S, w] = wt.useState([]), [b, U] = wt.useState(!1), [X, W] = wt.useState("Loading Auto Researcher Webview..."), [y, ce] = wt.useState(null), [B, K] = wt.useState("research"), [ye, ne] = wt.useState(null);
  wt.useEffect(() => {
    const Oe = new fv(pv), $e = (it) => {
      const Rt = it.data;
      switch (console.log("[Webview] Received message:", Rt), Rt.type) {
        case "init":
          W("Webview initialized successfully!");
          break;
        case "research-progress":
          V(Rt);
          break;
        case "research-started":
          oe(Rt);
          break;
        case "research-completed":
          $(Rt);
          break;
        case "research-error":
          de(Rt);
          break;
        case "hitl-request":
          Ae(Rt);
          break;
        default:
          console.log("[Webview] Unknown message type:", Rt.type);
      }
    };
    return window.addEventListener("message", $e), Oe.postMessage({ type: "webview-ready" }), () => {
      window.removeEventListener("message", $e);
    };
  }, []);
  const oe = (Oe) => {
    U(!0), w([]), W(`Research started: ${Oe.topic || "Unknown topic"}`);
  }, V = (Oe) => {
    const $e = {
      title: Ye(Oe.node || "processing"),
      data: Oe.message || Oe.data || ""
    };
    w((it) => [...it, $e]), W(`Processing: ${$e.title}`);
  }, $ = (Oe) => {
    U(!1);
    const $e = {
      title: "Research Completed",
      data: `Session ID: ${Oe.session_id}`
    };
    w((it) => [...it, $e]), W("Research completed successfully!");
  }, de = (Oe) => {
    U(!1);
    const $e = {
      title: "Research Error",
      data: Oe.error || "An error occurred"
    };
    w((it) => [...it, $e]), W(`Research failed: ${Oe.error}`);
  }, Ae = (Oe) => {
    ce(Oe), U(!1), W(`HITL Required: ${Oe.decision_type}`);
  }, Dt = (Oe, $e) => {
    if (!y)
      return;
    new fv(pv).sendHITLResponse(y.request_id, Oe, $e), ce(null), W(`HITL response sent: ${Oe}`);
  }, rt = (Oe) => {
    ne(Oe), K("session-detail");
  }, Ke = () => {
    ne(null), K("sessions");
  }, ct = () => {
    new fv(pv).startResearch("New Research Topic"), K("research");
  }, ke = (Oe, $e) => {
    new fv(pv).openPaper(Oe, $e);
  }, at = (Oe) => {
    new fv(pv).exportManuscript(Oe, "md");
  }, Ye = (Oe) => ({
    query_generation: "Generating Search Queries",
    query_approval: "Waiting for Query Approval",
    search_and_filter: "Searching and Filtering Papers",
    paper_selection: "Selecting Relevant Papers",
    paper_selection_approval: "Waiting for Paper Selection Approval",
    full_text_retrieval: "Retrieving Full-Text Papers",
    report_synthesis: "Synthesizing Research Report",
    final_report: "Finalizing Report",
    reflection_and_refinement: "Reflecting and Refining Strategy"
  })[Oe] || `Processing: ${Oe}`, be = () => {
    var Ie;
    if (!y)
      return null;
    const { decision_type: Oe, context: $e, request_id: it, timeout_seconds: Rt } = y;
    switch (Oe) {
      case "query_approval":
        return /* @__PURE__ */ C.jsx(
          hN,
          {
            requestId: it,
            prompt: y.prompt,
            queries: $e.queries || [],
            timeoutSeconds: Rt,
            researchTopic: $e.research_topic || "Research Topic",
            onResponse: Dt
          }
        );
      case "paper_selection":
        return /* @__PURE__ */ C.jsx(
          mN,
          {
            requestId: it,
            prompt: y.prompt,
            papers: $e.papers || [],
            totalCount: $e.total_count || ((Ie = $e.papers) == null ? void 0 : Ie.length) || 0,
            recommendation: $e.recommendation,
            timeoutSeconds: Rt,
            onResponse: Dt
          }
        );
      case "report_revision":
        return /* @__PURE__ */ C.jsx(
          yN,
          {
            requestId: it,
            prompt: y.prompt,
            report: $e.report || "",
            wordCount: $e.word_count || 0,
            paperCount: $e.paper_count || 0,
            researchTopic: $e.research_topic || "Research Topic",
            timeoutSeconds: Rt,
            onResponse: Dt
          }
        );
      default:
        return /* @__PURE__ */ C.jsxs("div", { className: "bg-neutral-700 rounded-lg border border-neutral-600 p-6 max-w-4xl mx-auto", children: [
          /* @__PURE__ */ C.jsxs("h2", { className: "text-xl font-semibold text-neutral-100 mb-4", children: [
            "Unknown HITL Request Type: ",
            Oe
          ] }),
          /* @__PURE__ */ C.jsx("pre", { className: "text-sm text-neutral-300 bg-neutral-800 p-4 rounded overflow-auto", children: JSON.stringify(y, null, 2) })
        ] });
    }
  };
  return /* @__PURE__ */ C.jsx("div", { className: "min-h-screen bg-neutral-800 text-neutral-100 p-4", children: /* @__PURE__ */ C.jsxs("div", { className: "max-w-4xl mx-auto", children: [
    /* @__PURE__ */ C.jsx("header", { className: "mb-6", children: /* @__PURE__ */ C.jsxs("div", { className: "flex items-center justify-between", children: [
      /* @__PURE__ */ C.jsxs("div", { children: [
        /* @__PURE__ */ C.jsx("h1", { className: "text-3xl font-bold text-primary", children: "🤖 Auto Researcher Webview" }),
        /* @__PURE__ */ C.jsx("p", { className: "text-neutral-400 mt-2", children: "React-based Collaboration UI for MCP-powered Research" })
      ] }),
      /* @__PURE__ */ C.jsxs("div", { className: "flex gap-2", children: [
        /* @__PURE__ */ C.jsx(
          "button",
          {
            onClick: () => K("research"),
            className: `px-4 py-2 rounded-md font-medium transition-colors ${B === "research" ? "bg-blue-600 text-white" : "bg-neutral-700 text-neutral-300 hover:bg-neutral-600"}`,
            children: "🔬 Research"
          }
        ),
        /* @__PURE__ */ C.jsx(
          "button",
          {
            onClick: () => K("sessions"),
            className: `px-4 py-2 rounded-md font-medium transition-colors ${B === "sessions" ? "bg-blue-600 text-white" : "bg-neutral-700 text-neutral-300 hover:bg-neutral-600"}`,
            children: "📚 Sessions"
          }
        )
      ] })
    ] }) }),
    /* @__PURE__ */ C.jsx("main", { className: "space-y-6", children: y ? be() : /* @__PURE__ */ C.jsxs(C.Fragment, { children: [
      B === "research" && /* @__PURE__ */ C.jsxs(C.Fragment, { children: [
        /* @__PURE__ */ C.jsx(
          vN,
          {
            processedEvents: S,
            isLoading: b
          }
        ),
        /* @__PURE__ */ C.jsxs("div", { className: "bg-neutral-700 p-6 rounded-lg border border-neutral-600", children: [
          /* @__PURE__ */ C.jsx("h2", { className: "text-xl font-semibold mb-4 text-neutral-100", children: "Debug Status" }),
          /* @__PURE__ */ C.jsx("p", { className: "text-sm text-neutral-300", children: X }),
          /* @__PURE__ */ C.jsxs("div", { className: "mt-4 text-xs text-neutral-400", children: [
            "Events: ",
            S.length,
            " | Loading: ",
            b ? "Yes" : "No"
          ] })
        ] })
      ] }),
      B === "sessions" && /* @__PURE__ */ C.jsx(
        gN,
        {
          onSelectSession: rt,
          onCreateNewSession: ct
        }
      ),
      B === "session-detail" && ye && /* @__PURE__ */ C.jsx(
        SN,
        {
          sessionId: ye,
          onBack: Ke,
          onOpenPaper: ke,
          onExportReport: at
        }
      )
    ] }) })
  ] }) });
};
hv.createRoot(document.getElementById("root")).render(
  /* @__PURE__ */ C.jsx(G_.StrictMode, { children: /* @__PURE__ */ C.jsx(xN, {}) })
);
//# sourceMappingURL=webview.js.map
