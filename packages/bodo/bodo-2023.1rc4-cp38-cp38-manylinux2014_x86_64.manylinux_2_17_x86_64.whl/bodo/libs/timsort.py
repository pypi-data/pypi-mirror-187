import numba
import numpy as np
import pandas as pd
from numba.extending import overload
from bodo.utils.utils import alloc_arr_tup
MIN_MERGE = 32


@numba.njit(no_cpython_wrapper=True, cache=True)
def sort(key_arrs, lo, hi, data):
    bvt__ovyp = hi - lo
    if bvt__ovyp < 2:
        return
    if bvt__ovyp < MIN_MERGE:
        vjlle__lty = countRunAndMakeAscending(key_arrs, lo, hi, data)
        binarySort(key_arrs, lo, hi, lo + vjlle__lty, data)
        return
    stackSize, runBase, runLen, tmpLength, tmp, tmp_data, minGallop = (
        init_sort_start(key_arrs, data))
    hgplk__lqrys = minRunLength(bvt__ovyp)
    while True:
        imf__avf = countRunAndMakeAscending(key_arrs, lo, hi, data)
        if imf__avf < hgplk__lqrys:
            cikbf__hiddr = (bvt__ovyp if bvt__ovyp <= hgplk__lqrys else
                hgplk__lqrys)
            binarySort(key_arrs, lo, lo + cikbf__hiddr, lo + imf__avf, data)
            imf__avf = cikbf__hiddr
        stackSize = pushRun(stackSize, runBase, runLen, lo, imf__avf)
        stackSize, tmpLength, tmp, tmp_data, minGallop = mergeCollapse(
            stackSize, runBase, runLen, key_arrs, data, tmpLength, tmp,
            tmp_data, minGallop)
        lo += imf__avf
        bvt__ovyp -= imf__avf
        if bvt__ovyp == 0:
            break
    assert lo == hi
    stackSize, tmpLength, tmp, tmp_data, minGallop = mergeForceCollapse(
        stackSize, runBase, runLen, key_arrs, data, tmpLength, tmp,
        tmp_data, minGallop)
    assert stackSize == 1


@numba.njit(no_cpython_wrapper=True, cache=True)
def binarySort(key_arrs, lo, hi, start, data):
    assert lo <= start and start <= hi
    if start == lo:
        start += 1
    while start < hi:
        uyh__gvfm = getitem_arr_tup(key_arrs, start)
        nkth__hcxw = getitem_arr_tup(data, start)
        osui__duxb = lo
        gttb__ceiv = start
        assert osui__duxb <= gttb__ceiv
        while osui__duxb < gttb__ceiv:
            ufxf__nyvb = osui__duxb + gttb__ceiv >> 1
            if uyh__gvfm < getitem_arr_tup(key_arrs, ufxf__nyvb):
                gttb__ceiv = ufxf__nyvb
            else:
                osui__duxb = ufxf__nyvb + 1
        assert osui__duxb == gttb__ceiv
        n = start - osui__duxb
        copyRange_tup(key_arrs, osui__duxb, key_arrs, osui__duxb + 1, n)
        copyRange_tup(data, osui__duxb, data, osui__duxb + 1, n)
        setitem_arr_tup(key_arrs, osui__duxb, uyh__gvfm)
        setitem_arr_tup(data, osui__duxb, nkth__hcxw)
        start += 1


@numba.njit(no_cpython_wrapper=True, cache=True)
def countRunAndMakeAscending(key_arrs, lo, hi, data):
    assert lo < hi
    sscm__llpn = lo + 1
    if sscm__llpn == hi:
        return 1
    if getitem_arr_tup(key_arrs, sscm__llpn) < getitem_arr_tup(key_arrs, lo):
        sscm__llpn += 1
        while sscm__llpn < hi and getitem_arr_tup(key_arrs, sscm__llpn
            ) < getitem_arr_tup(key_arrs, sscm__llpn - 1):
            sscm__llpn += 1
        reverseRange(key_arrs, lo, sscm__llpn, data)
    else:
        sscm__llpn += 1
        while sscm__llpn < hi and getitem_arr_tup(key_arrs, sscm__llpn
            ) >= getitem_arr_tup(key_arrs, sscm__llpn - 1):
            sscm__llpn += 1
    return sscm__llpn - lo


@numba.njit(no_cpython_wrapper=True, cache=True)
def reverseRange(key_arrs, lo, hi, data):
    hi -= 1
    while lo < hi:
        swap_arrs(key_arrs, lo, hi)
        swap_arrs(data, lo, hi)
        lo += 1
        hi -= 1


@numba.njit(no_cpython_wrapper=True, cache=True)
def minRunLength(n):
    assert n >= 0
    widb__wnuf = 0
    while n >= MIN_MERGE:
        widb__wnuf |= n & 1
        n >>= 1
    return n + widb__wnuf


MIN_GALLOP = 7
INITIAL_TMP_STORAGE_LENGTH = 256


@numba.njit(no_cpython_wrapper=True, cache=True)
def init_sort_start(key_arrs, data):
    minGallop = MIN_GALLOP
    buszg__ctoc = len(key_arrs[0])
    tmpLength = (buszg__ctoc >> 1 if buszg__ctoc < 2 *
        INITIAL_TMP_STORAGE_LENGTH else INITIAL_TMP_STORAGE_LENGTH)
    tmp = alloc_arr_tup(tmpLength, key_arrs)
    tmp_data = alloc_arr_tup(tmpLength, data)
    stackSize = 0
    jtj__rxtao = (5 if buszg__ctoc < 120 else 10 if buszg__ctoc < 1542 else
        19 if buszg__ctoc < 119151 else 40)
    runBase = np.empty(jtj__rxtao, np.int64)
    runLen = np.empty(jtj__rxtao, np.int64)
    return stackSize, runBase, runLen, tmpLength, tmp, tmp_data, minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def pushRun(stackSize, runBase, runLen, runBase_val, runLen_val):
    runBase[stackSize] = runBase_val
    runLen[stackSize] = runLen_val
    stackSize += 1
    return stackSize


@numba.njit(no_cpython_wrapper=True, cache=True)
def mergeCollapse(stackSize, runBase, runLen, key_arrs, data, tmpLength,
    tmp, tmp_data, minGallop):
    while stackSize > 1:
        n = stackSize - 2
        if n >= 1 and runLen[n - 1] <= runLen[n] + runLen[n + 1
            ] or n >= 2 and runLen[n - 2] <= runLen[n] + runLen[n - 1]:
            if runLen[n - 1] < runLen[n + 1]:
                n -= 1
        elif runLen[n] > runLen[n + 1]:
            break
        stackSize, tmpLength, tmp, tmp_data, minGallop = mergeAt(stackSize,
            runBase, runLen, key_arrs, data, tmpLength, tmp, tmp_data,
            minGallop, n)
    return stackSize, tmpLength, tmp, tmp_data, minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def mergeForceCollapse(stackSize, runBase, runLen, key_arrs, data,
    tmpLength, tmp, tmp_data, minGallop):
    while stackSize > 1:
        n = stackSize - 2
        if n > 0 and runLen[n - 1] < runLen[n + 1]:
            n -= 1
        stackSize, tmpLength, tmp, tmp_data, minGallop = mergeAt(stackSize,
            runBase, runLen, key_arrs, data, tmpLength, tmp, tmp_data,
            minGallop, n)
    return stackSize, tmpLength, tmp, tmp_data, minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def mergeAt(stackSize, runBase, runLen, key_arrs, data, tmpLength, tmp,
    tmp_data, minGallop, i):
    assert stackSize >= 2
    assert i >= 0
    assert i == stackSize - 2 or i == stackSize - 3
    base1 = runBase[i]
    len1 = runLen[i]
    base2 = runBase[i + 1]
    len2 = runLen[i + 1]
    assert len1 > 0 and len2 > 0
    assert base1 + len1 == base2
    runLen[i] = len1 + len2
    if i == stackSize - 3:
        runBase[i + 1] = runBase[i + 2]
        runLen[i + 1] = runLen[i + 2]
    stackSize -= 1
    swpy__tskk = gallopRight(getitem_arr_tup(key_arrs, base2), key_arrs,
        base1, len1, 0)
    assert swpy__tskk >= 0
    base1 += swpy__tskk
    len1 -= swpy__tskk
    if len1 == 0:
        return stackSize, tmpLength, tmp, tmp_data, minGallop
    len2 = gallopLeft(getitem_arr_tup(key_arrs, base1 + len1 - 1), key_arrs,
        base2, len2, len2 - 1)
    assert len2 >= 0
    if len2 == 0:
        return stackSize, tmpLength, tmp, tmp_data, minGallop
    if len1 <= len2:
        tmpLength, tmp, tmp_data = ensureCapacity(tmpLength, tmp, tmp_data,
            key_arrs, data, len1)
        minGallop = mergeLo(key_arrs, data, tmp, tmp_data, minGallop, base1,
            len1, base2, len2)
    else:
        tmpLength, tmp, tmp_data = ensureCapacity(tmpLength, tmp, tmp_data,
            key_arrs, data, len2)
        minGallop = mergeHi(key_arrs, data, tmp, tmp_data, minGallop, base1,
            len1, base2, len2)
    return stackSize, tmpLength, tmp, tmp_data, minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def gallopLeft(key, arr, base, _len, hint):
    assert _len > 0 and hint >= 0 and hint < _len
    mzfi__jwqss = 0
    tvp__cway = 1
    if key > getitem_arr_tup(arr, base + hint):
        popso__znvxs = _len - hint
        while tvp__cway < popso__znvxs and key > getitem_arr_tup(arr, base +
            hint + tvp__cway):
            mzfi__jwqss = tvp__cway
            tvp__cway = (tvp__cway << 1) + 1
            if tvp__cway <= 0:
                tvp__cway = popso__znvxs
        if tvp__cway > popso__znvxs:
            tvp__cway = popso__znvxs
        mzfi__jwqss += hint
        tvp__cway += hint
    else:
        popso__znvxs = hint + 1
        while tvp__cway < popso__znvxs and key <= getitem_arr_tup(arr, base +
            hint - tvp__cway):
            mzfi__jwqss = tvp__cway
            tvp__cway = (tvp__cway << 1) + 1
            if tvp__cway <= 0:
                tvp__cway = popso__znvxs
        if tvp__cway > popso__znvxs:
            tvp__cway = popso__znvxs
        tmp = mzfi__jwqss
        mzfi__jwqss = hint - tvp__cway
        tvp__cway = hint - tmp
    assert -1 <= mzfi__jwqss and mzfi__jwqss < tvp__cway and tvp__cway <= _len
    mzfi__jwqss += 1
    while mzfi__jwqss < tvp__cway:
        dztlr__lom = mzfi__jwqss + (tvp__cway - mzfi__jwqss >> 1)
        if key > getitem_arr_tup(arr, base + dztlr__lom):
            mzfi__jwqss = dztlr__lom + 1
        else:
            tvp__cway = dztlr__lom
    assert mzfi__jwqss == tvp__cway
    return tvp__cway


@numba.njit(no_cpython_wrapper=True, cache=True)
def gallopRight(key, arr, base, _len, hint):
    assert _len > 0 and hint >= 0 and hint < _len
    tvp__cway = 1
    mzfi__jwqss = 0
    if key < getitem_arr_tup(arr, base + hint):
        popso__znvxs = hint + 1
        while tvp__cway < popso__znvxs and key < getitem_arr_tup(arr, base +
            hint - tvp__cway):
            mzfi__jwqss = tvp__cway
            tvp__cway = (tvp__cway << 1) + 1
            if tvp__cway <= 0:
                tvp__cway = popso__znvxs
        if tvp__cway > popso__znvxs:
            tvp__cway = popso__znvxs
        tmp = mzfi__jwqss
        mzfi__jwqss = hint - tvp__cway
        tvp__cway = hint - tmp
    else:
        popso__znvxs = _len - hint
        while tvp__cway < popso__znvxs and key >= getitem_arr_tup(arr, base +
            hint + tvp__cway):
            mzfi__jwqss = tvp__cway
            tvp__cway = (tvp__cway << 1) + 1
            if tvp__cway <= 0:
                tvp__cway = popso__znvxs
        if tvp__cway > popso__znvxs:
            tvp__cway = popso__znvxs
        mzfi__jwqss += hint
        tvp__cway += hint
    assert -1 <= mzfi__jwqss and mzfi__jwqss < tvp__cway and tvp__cway <= _len
    mzfi__jwqss += 1
    while mzfi__jwqss < tvp__cway:
        dztlr__lom = mzfi__jwqss + (tvp__cway - mzfi__jwqss >> 1)
        if key < getitem_arr_tup(arr, base + dztlr__lom):
            tvp__cway = dztlr__lom
        else:
            mzfi__jwqss = dztlr__lom + 1
    assert mzfi__jwqss == tvp__cway
    return tvp__cway


@numba.njit(no_cpython_wrapper=True, cache=True)
def mergeLo(key_arrs, data, tmp, tmp_data, minGallop, base1, len1, base2, len2
    ):
    assert len1 > 0 and len2 > 0 and base1 + len1 == base2
    arr = key_arrs
    arr_data = data
    copyRange_tup(arr, base1, tmp, 0, len1)
    copyRange_tup(arr_data, base1, tmp_data, 0, len1)
    cursor1 = 0
    cursor2 = base2
    dest = base1
    setitem_arr_tup(arr, dest, getitem_arr_tup(arr, cursor2))
    copyElement_tup(arr_data, cursor2, arr_data, dest)
    cursor2 += 1
    dest += 1
    len2 -= 1
    if len2 == 0:
        copyRange_tup(tmp, cursor1, arr, dest, len1)
        copyRange_tup(tmp_data, cursor1, arr_data, dest, len1)
        return minGallop
    if len1 == 1:
        copyRange_tup(arr, cursor2, arr, dest, len2)
        copyRange_tup(arr_data, cursor2, arr_data, dest, len2)
        copyElement_tup(tmp, cursor1, arr, dest + len2)
        copyElement_tup(tmp_data, cursor1, arr_data, dest + len2)
        return minGallop
    len1, len2, cursor1, cursor2, dest, minGallop = mergeLo_inner(key_arrs,
        data, tmp_data, len1, len2, tmp, cursor1, cursor2, dest, minGallop)
    minGallop = 1 if minGallop < 1 else minGallop
    if len1 == 1:
        assert len2 > 0
        copyRange_tup(arr, cursor2, arr, dest, len2)
        copyRange_tup(arr_data, cursor2, arr_data, dest, len2)
        copyElement_tup(tmp, cursor1, arr, dest + len2)
        copyElement_tup(tmp_data, cursor1, arr_data, dest + len2)
    elif len1 == 0:
        raise ValueError('Comparison method violates its general contract!')
    else:
        assert len2 == 0
        assert len1 > 1
        copyRange_tup(tmp, cursor1, arr, dest, len1)
        copyRange_tup(tmp_data, cursor1, arr_data, dest, len1)
    return minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def mergeLo_inner(arr, arr_data, tmp_data, len1, len2, tmp, cursor1,
    cursor2, dest, minGallop):
    while True:
        mkhn__why = 0
        kzk__mbawa = 0
        while True:
            assert len1 > 1 and len2 > 0
            if getitem_arr_tup(arr, cursor2) < getitem_arr_tup(tmp, cursor1):
                copyElement_tup(arr, cursor2, arr, dest)
                copyElement_tup(arr_data, cursor2, arr_data, dest)
                cursor2 += 1
                dest += 1
                kzk__mbawa += 1
                mkhn__why = 0
                len2 -= 1
                if len2 == 0:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            else:
                copyElement_tup(tmp, cursor1, arr, dest)
                copyElement_tup(tmp_data, cursor1, arr_data, dest)
                cursor1 += 1
                dest += 1
                mkhn__why += 1
                kzk__mbawa = 0
                len1 -= 1
                if len1 == 1:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            if not mkhn__why | kzk__mbawa < minGallop:
                break
        while True:
            assert len1 > 1 and len2 > 0
            mkhn__why = gallopRight(getitem_arr_tup(arr, cursor2), tmp,
                cursor1, len1, 0)
            if mkhn__why != 0:
                copyRange_tup(tmp, cursor1, arr, dest, mkhn__why)
                copyRange_tup(tmp_data, cursor1, arr_data, dest, mkhn__why)
                dest += mkhn__why
                cursor1 += mkhn__why
                len1 -= mkhn__why
                if len1 <= 1:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            copyElement_tup(arr, cursor2, arr, dest)
            copyElement_tup(arr_data, cursor2, arr_data, dest)
            cursor2 += 1
            dest += 1
            len2 -= 1
            if len2 == 0:
                return len1, len2, cursor1, cursor2, dest, minGallop
            kzk__mbawa = gallopLeft(getitem_arr_tup(tmp, cursor1), arr,
                cursor2, len2, 0)
            if kzk__mbawa != 0:
                copyRange_tup(arr, cursor2, arr, dest, kzk__mbawa)
                copyRange_tup(arr_data, cursor2, arr_data, dest, kzk__mbawa)
                dest += kzk__mbawa
                cursor2 += kzk__mbawa
                len2 -= kzk__mbawa
                if len2 == 0:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            copyElement_tup(tmp, cursor1, arr, dest)
            copyElement_tup(tmp_data, cursor1, arr_data, dest)
            cursor1 += 1
            dest += 1
            len1 -= 1
            if len1 == 1:
                return len1, len2, cursor1, cursor2, dest, minGallop
            minGallop -= 1
            if not mkhn__why >= MIN_GALLOP | kzk__mbawa >= MIN_GALLOP:
                break
        if minGallop < 0:
            minGallop = 0
        minGallop += 2
    return len1, len2, cursor1, cursor2, dest, minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def mergeHi(key_arrs, data, tmp, tmp_data, minGallop, base1, len1, base2, len2
    ):
    assert len1 > 0 and len2 > 0 and base1 + len1 == base2
    arr = key_arrs
    arr_data = data
    copyRange_tup(arr, base2, tmp, 0, len2)
    copyRange_tup(arr_data, base2, tmp_data, 0, len2)
    cursor1 = base1 + len1 - 1
    cursor2 = len2 - 1
    dest = base2 + len2 - 1
    copyElement_tup(arr, cursor1, arr, dest)
    copyElement_tup(arr_data, cursor1, arr_data, dest)
    cursor1 -= 1
    dest -= 1
    len1 -= 1
    if len1 == 0:
        copyRange_tup(tmp, 0, arr, dest - (len2 - 1), len2)
        copyRange_tup(tmp_data, 0, arr_data, dest - (len2 - 1), len2)
        return minGallop
    if len2 == 1:
        dest -= len1
        cursor1 -= len1
        copyRange_tup(arr, cursor1 + 1, arr, dest + 1, len1)
        copyRange_tup(arr_data, cursor1 + 1, arr_data, dest + 1, len1)
        copyElement_tup(tmp, cursor2, arr, dest)
        copyElement_tup(tmp_data, cursor2, arr_data, dest)
        return minGallop
    len1, len2, tmp, cursor1, cursor2, dest, minGallop = mergeHi_inner(key_arrs
        , data, tmp_data, base1, len1, len2, tmp, cursor1, cursor2, dest,
        minGallop)
    minGallop = 1 if minGallop < 1 else minGallop
    if len2 == 1:
        assert len1 > 0
        dest -= len1
        cursor1 -= len1
        copyRange_tup(arr, cursor1 + 1, arr, dest + 1, len1)
        copyRange_tup(arr_data, cursor1 + 1, arr_data, dest + 1, len1)
        copyElement_tup(tmp, cursor2, arr, dest)
        copyElement_tup(tmp_data, cursor2, arr_data, dest)
    elif len2 == 0:
        raise ValueError('Comparison method violates its general contract!')
    else:
        assert len1 == 0
        assert len2 > 0
        copyRange_tup(tmp, 0, arr, dest - (len2 - 1), len2)
        copyRange_tup(tmp_data, 0, arr_data, dest - (len2 - 1), len2)
    return minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def mergeHi_inner(arr, arr_data, tmp_data, base1, len1, len2, tmp, cursor1,
    cursor2, dest, minGallop):
    while True:
        mkhn__why = 0
        kzk__mbawa = 0
        while True:
            assert len1 > 0 and len2 > 1
            if getitem_arr_tup(tmp, cursor2) < getitem_arr_tup(arr, cursor1):
                copyElement_tup(arr, cursor1, arr, dest)
                copyElement_tup(arr_data, cursor1, arr_data, dest)
                cursor1 -= 1
                dest -= 1
                mkhn__why += 1
                kzk__mbawa = 0
                len1 -= 1
                if len1 == 0:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            else:
                copyElement_tup(tmp, cursor2, arr, dest)
                copyElement_tup(tmp_data, cursor2, arr_data, dest)
                cursor2 -= 1
                dest -= 1
                kzk__mbawa += 1
                mkhn__why = 0
                len2 -= 1
                if len2 == 1:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            if not mkhn__why | kzk__mbawa < minGallop:
                break
        while True:
            assert len1 > 0 and len2 > 1
            mkhn__why = len1 - gallopRight(getitem_arr_tup(tmp, cursor2),
                arr, base1, len1, len1 - 1)
            if mkhn__why != 0:
                dest -= mkhn__why
                cursor1 -= mkhn__why
                len1 -= mkhn__why
                copyRange_tup(arr, cursor1 + 1, arr, dest + 1, mkhn__why)
                copyRange_tup(arr_data, cursor1 + 1, arr_data, dest + 1,
                    mkhn__why)
                if len1 == 0:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            copyElement_tup(tmp, cursor2, arr, dest)
            copyElement_tup(tmp_data, cursor2, arr_data, dest)
            cursor2 -= 1
            dest -= 1
            len2 -= 1
            if len2 == 1:
                return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            kzk__mbawa = len2 - gallopLeft(getitem_arr_tup(arr, cursor1),
                tmp, 0, len2, len2 - 1)
            if kzk__mbawa != 0:
                dest -= kzk__mbawa
                cursor2 -= kzk__mbawa
                len2 -= kzk__mbawa
                copyRange_tup(tmp, cursor2 + 1, arr, dest + 1, kzk__mbawa)
                copyRange_tup(tmp_data, cursor2 + 1, arr_data, dest + 1,
                    kzk__mbawa)
                if len2 <= 1:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            copyElement_tup(arr, cursor1, arr, dest)
            copyElement_tup(arr_data, cursor1, arr_data, dest)
            cursor1 -= 1
            dest -= 1
            len1 -= 1
            if len1 == 0:
                return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            minGallop -= 1
            if not mkhn__why >= MIN_GALLOP | kzk__mbawa >= MIN_GALLOP:
                break
        if minGallop < 0:
            minGallop = 0
        minGallop += 2
    return len1, len2, tmp, cursor1, cursor2, dest, minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def ensureCapacity(tmpLength, tmp, tmp_data, key_arrs, data, minCapacity):
    kylao__ajdg = len(key_arrs[0])
    if tmpLength < minCapacity:
        mmmg__ornq = minCapacity
        mmmg__ornq |= mmmg__ornq >> 1
        mmmg__ornq |= mmmg__ornq >> 2
        mmmg__ornq |= mmmg__ornq >> 4
        mmmg__ornq |= mmmg__ornq >> 8
        mmmg__ornq |= mmmg__ornq >> 16
        mmmg__ornq += 1
        if mmmg__ornq < 0:
            mmmg__ornq = minCapacity
        else:
            mmmg__ornq = min(mmmg__ornq, kylao__ajdg >> 1)
        tmp = alloc_arr_tup(mmmg__ornq, key_arrs)
        tmp_data = alloc_arr_tup(mmmg__ornq, data)
        tmpLength = mmmg__ornq
    return tmpLength, tmp, tmp_data


def swap_arrs(data, lo, hi):
    for arr in data:
        xmjtm__swatz = arr[lo]
        arr[lo] = arr[hi]
        arr[hi] = xmjtm__swatz


@overload(swap_arrs, no_unliteral=True)
def swap_arrs_overload(arr_tup, lo, hi):
    tei__tvkk = arr_tup.count
    aiph__uubdi = 'def f(arr_tup, lo, hi):\n'
    for i in range(tei__tvkk):
        aiph__uubdi += '  tmp_v_{} = arr_tup[{}][lo]\n'.format(i, i)
        aiph__uubdi += '  arr_tup[{}][lo] = arr_tup[{}][hi]\n'.format(i, i)
        aiph__uubdi += '  arr_tup[{}][hi] = tmp_v_{}\n'.format(i, i)
    aiph__uubdi += '  return\n'
    wgvu__rrycq = {}
    exec(aiph__uubdi, {}, wgvu__rrycq)
    xkpex__hqb = wgvu__rrycq['f']
    return xkpex__hqb


@numba.njit(no_cpython_wrapper=True, cache=True)
def copyRange(src_arr, src_pos, dst_arr, dst_pos, n):
    dst_arr[dst_pos:dst_pos + n] = src_arr[src_pos:src_pos + n]


def copyRange_tup(src_arr_tup, src_pos, dst_arr_tup, dst_pos, n):
    for src_arr, dst_arr in zip(src_arr_tup, dst_arr_tup):
        dst_arr[dst_pos:dst_pos + n] = src_arr[src_pos:src_pos + n]


@overload(copyRange_tup, no_unliteral=True)
def copyRange_tup_overload(src_arr_tup, src_pos, dst_arr_tup, dst_pos, n):
    tei__tvkk = src_arr_tup.count
    assert tei__tvkk == dst_arr_tup.count
    aiph__uubdi = 'def f(src_arr_tup, src_pos, dst_arr_tup, dst_pos, n):\n'
    for i in range(tei__tvkk):
        aiph__uubdi += (
            '  copyRange(src_arr_tup[{}], src_pos, dst_arr_tup[{}], dst_pos, n)\n'
            .format(i, i))
    aiph__uubdi += '  return\n'
    wgvu__rrycq = {}
    exec(aiph__uubdi, {'copyRange': copyRange}, wgvu__rrycq)
    ublt__iogku = wgvu__rrycq['f']
    return ublt__iogku


@numba.njit(no_cpython_wrapper=True, cache=True)
def copyElement(src_arr, src_pos, dst_arr, dst_pos):
    dst_arr[dst_pos] = src_arr[src_pos]


def copyElement_tup(src_arr_tup, src_pos, dst_arr_tup, dst_pos):
    for src_arr, dst_arr in zip(src_arr_tup, dst_arr_tup):
        dst_arr[dst_pos] = src_arr[src_pos]


@overload(copyElement_tup, no_unliteral=True)
def copyElement_tup_overload(src_arr_tup, src_pos, dst_arr_tup, dst_pos):
    tei__tvkk = src_arr_tup.count
    assert tei__tvkk == dst_arr_tup.count
    aiph__uubdi = 'def f(src_arr_tup, src_pos, dst_arr_tup, dst_pos):\n'
    for i in range(tei__tvkk):
        aiph__uubdi += (
            '  copyElement(src_arr_tup[{}], src_pos, dst_arr_tup[{}], dst_pos)\n'
            .format(i, i))
    aiph__uubdi += '  return\n'
    wgvu__rrycq = {}
    exec(aiph__uubdi, {'copyElement': copyElement}, wgvu__rrycq)
    ublt__iogku = wgvu__rrycq['f']
    return ublt__iogku


def getitem_arr_tup(arr_tup, ind):
    komqj__beio = [arr[ind] for arr in arr_tup]
    return tuple(komqj__beio)


@overload(getitem_arr_tup, no_unliteral=True)
def getitem_arr_tup_overload(arr_tup, ind):
    tei__tvkk = arr_tup.count
    aiph__uubdi = 'def f(arr_tup, ind):\n'
    aiph__uubdi += '  return ({}{})\n'.format(','.join(['arr_tup[{}][ind]'.
        format(i) for i in range(tei__tvkk)]), ',' if tei__tvkk == 1 else '')
    wgvu__rrycq = {}
    exec(aiph__uubdi, {}, wgvu__rrycq)
    wop__eaa = wgvu__rrycq['f']
    return wop__eaa


def setitem_arr_tup(arr_tup, ind, val_tup):
    for arr, qnq__zothm in zip(arr_tup, val_tup):
        arr[ind] = qnq__zothm


@overload(setitem_arr_tup, no_unliteral=True)
def setitem_arr_tup_overload(arr_tup, ind, val_tup):
    tei__tvkk = arr_tup.count
    aiph__uubdi = 'def f(arr_tup, ind, val_tup):\n'
    for i in range(tei__tvkk):
        if isinstance(val_tup, numba.core.types.BaseTuple):
            aiph__uubdi += '  arr_tup[{}][ind] = val_tup[{}]\n'.format(i, i)
        else:
            assert arr_tup.count == 1
            aiph__uubdi += '  arr_tup[{}][ind] = val_tup\n'.format(i)
    aiph__uubdi += '  return\n'
    wgvu__rrycq = {}
    exec(aiph__uubdi, {}, wgvu__rrycq)
    wop__eaa = wgvu__rrycq['f']
    return wop__eaa


def test():
    import time
    yjb__ywse = time.time()
    jep__nfuds = np.ones(3)
    data = np.arange(3), np.ones(3)
    sort((jep__nfuds,), 0, 3, data)
    print('compile time', time.time() - yjb__ywse)
    n = 210000
    np.random.seed(2)
    data = np.arange(n), np.random.ranf(n)
    yhae__uoyz = np.random.ranf(n)
    qwv__vyhxy = pd.DataFrame({'A': yhae__uoyz, 'B': data[0], 'C': data[1]})
    yjb__ywse = time.time()
    qrf__ubys = qwv__vyhxy.sort_values('A', inplace=False)
    vww__zddn = time.time()
    sort((yhae__uoyz,), 0, n, data)
    print('Bodo', time.time() - vww__zddn, 'Numpy', vww__zddn - yjb__ywse)
    np.testing.assert_almost_equal(data[0], qrf__ubys.B.values)
    np.testing.assert_almost_equal(data[1], qrf__ubys.C.values)


if __name__ == '__main__':
    test()
