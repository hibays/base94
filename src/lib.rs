// lib.rs
// Implementation of Base94 encode and decode in Rust for Python 3.
//
// THE GPLv3 LICENSE
// Copyleft (©) 2025 hibays
//

use pyo3::prelude::*;
use lazy_static::lazy_static;

lazy_static! {
    // Base94 字母表（与 Python 实现完全一致）
    static ref B94_ENCODE_TAB: Vec<u8> = vec![
        b'A', b'B', b'C', b'D', b'E', b'F', b'G', b'H', b'I', b'J', b'K', b'L', b'M',
        b'N', b'O', b'P', b'Q', b'R', b'S', b'T', b'U', b'V', b'W', b'X', b'Y', b'Z',
        b'a', b'b', b'c', b'd', b'e', b'f', b'g', b'h', b'i', b'j', b'k', b'l', b'm',
        b'n', b'o', b'p', b'q', b'r', b's', b't', b'u', b'v', b'w', b'x', b'y', b'z',
        b'0', b'1', b'2', b'3', b'4', b'5', b'6', b'7', b'8', b'9', b'!', b'"', b'#',
        b'$', b'%', b'&', b'\'', b'(', b')', b'*', b'+', b',', b'-', b'.', b'/', b':',
        b';', b'<', b'=', b'>', b'?', b'@', b'[', b'\\', b']', b'^', b'_', b'`', b'{',
        b'|', b'}', b'~'
    ];

    // 快速解码表（256 长度数组，直接通过 ASCII 值索引）
    static ref B94_DECODE_TAB: [u8; 256] = {
        let mut tab = [0xFF; 256];
        for (i, &c) in B94_ENCODE_TAB.iter().enumerate() {
            tab[c as usize] = i as u8;
        }
        tab
    };

    // 预生成双字符编码表（94x94 组合）
    static ref B94_ENCODE_TAB2: Vec<[u8; 2]> = {
        let mut tab = Vec::with_capacity(94*94);
        for &c1 in B94_ENCODE_TAB.iter() {
            for &c2 in B94_ENCODE_TAB.iter() {
                tab.push([c1, c2]);
            }
        }
        tab
    };
}

/// Base94 编码（Rust 加速版）
fn b94_encode_rust(data: &[u8]) -> Vec<u8> {
    let orig_len = data.len();
    let padding = (9 - (orig_len % 9)) % 9;
    let data = if padding > 0 {
        let mut padded = data.to_vec();
        padded.extend(vec![0u8; padding]);
        padded
    } else {
        data.to_vec()
    };

    let mut output = Vec::with_capacity((data.len() / 9) * 11);
    for chunk in data.chunks(9) {
        // 将 9 字节转换为大端 u128
        let mut n_bytes = [0u8; 16];
        n_bytes[7..16].copy_from_slice(chunk);
        let n = u128::from_be_bytes(n_bytes);

        // 分解为 6 个部分
        let (d8_9, rem1) = (n / 94, (n % 94) as usize);
        let (d6_7, rem2) = (d8_9 / 8836, (d8_9 % 8836) as usize);
        let (d4_5, rem3) = (d6_7 / 8836, (d6_7 % 8836) as usize);
        let (d2_3, rem4) = (d4_5 / 8836, (d4_5 % 8836) as usize);
        let (d1, rem5) = (d2_3 / 8836, (d2_3 % 8836) as usize);

        // 查表组合结果
        output.extend_from_slice(&B94_ENCODE_TAB2[d1 as usize]);
        output.extend_from_slice(&B94_ENCODE_TAB2[rem5]);
        output.extend_from_slice(&B94_ENCODE_TAB2[rem4]);
        output.extend_from_slice(&B94_ENCODE_TAB2[rem3]);
        output.extend_from_slice(&B94_ENCODE_TAB2[rem2]);
        output.push(B94_ENCODE_TAB[rem1]);
    }

    // 移除填充
    if padding > 0 {
        let len = output.len();
        output.truncate(len - padding);
    }
    output
}

/// Base94 解码（Rust 加速版）
fn b94_decode_rust(data: &[u8]) -> Result<Vec<u8>, String> {
    let orig_len = data.len();
    let padding = (11 - (orig_len % 11)) % 11;
    let data = if padding > 0 {
        let mut padded = data.to_vec();
        padded.extend(vec![b'~'; padding]);
        padded
    } else {
        data.to_vec()
    };

    let mut output = Vec::with_capacity((data.len() / 11) * 9);
    for chunk in data.chunks(11) {
        let mut num = 0u128;
        for &c in chunk {
            let digit = B94_DECODE_TAB[c as usize];
            if digit == 0xFF {
                return Err(format!("Invalid character: {}", c as char));
            }
            num = num * 94 + digit as u128;
        }

        // 将 u128 转换回 9 字节大端格式
        let bytes = num.to_be_bytes();
        output.extend_from_slice(&bytes[7..16]);
    }

    // 移除填充
    if padding > 0 {
        let len = output.len();
        output.truncate(len - padding);
    }
    Ok(output)
}

// PyO3 绑定
#[pyfunction]
fn b94encode(data: &[u8]) -> PyResult<Vec<u8>> {
    Ok(b94_encode_rust(data))
}

#[pyfunction]
fn b94decode(data: &[u8]) -> PyResult<Vec<u8>> {
    b94_decode_rust(data).map_err(|e| PyErr::new::<pyo3::exceptions::PyValueError, _>(e))
}

#[pymodule]
fn _base94(_py: Python<'_>, module: &Bound<'_, PyModule>) -> PyResult<()> {
    module.add_function(wrap_pyfunction!(b94encode, module)?)?;
    module.add_function(wrap_pyfunction!(b94decode, module)?)?;
    Ok(())
}