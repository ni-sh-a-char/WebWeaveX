package io.webweavex.crypto;

/**
 * Byte {@code _proc} bridge aligned with the {@code kaalka} v5.0.0 cipher path
 * (the JavaScript/Dart {@code kaalka_v5_proc}). A position-dependent modular
 * offset derived from an {@code HH:MM:SS} time key is added (encrypt) or
 * subtracted (decrypt) from each byte, modulo 256.
 */
public final class KaalkaV5Proc {

    private KaalkaV5Proc() {
    }

    /** Parsed {@code HH:MM:SS} time key (hours folded into {@code [0,12)}). */
    public static int[] parseKaalkaTimeKey(String timeKey) {
        String[] parts = timeKey.split(":");
        int hh = 0;
        int mm = 0;
        int ss = 0;
        if (parts.length == 3) {
            hh = Integer.parseInt(parts[0]);
            mm = Integer.parseInt(parts[1]);
            ss = Integer.parseInt(parts[2]);
        } else if (parts.length == 2) {
            mm = Integer.parseInt(parts[0]);
            ss = Integer.parseInt(parts[1]);
        } else if (parts.length == 1 && !parts[0].isEmpty()) {
            ss = Integer.parseInt(parts[0]);
        }
        return new int[] {Math.floorMod(hh, 12), mm, ss};
    }

    private static byte[] proc(byte[] data, boolean encrypt, int h, int m, int s) {
        int seconds = h * 3600 + m * 60 + s;
        int key = seconds == 0 ? 1 : seconds;
        byte[] out = new byte[data.length];
        for (int idx = 0; idx < data.length; idx++) {
            int b = data[idx] & 0xFF;
            int offset = Math.floorMod(key + idx, 256);
            int val = encrypt ? Math.floorMod(b + offset, 256) : Math.floorMod(b - offset, 256);
            out[idx] = (byte) val;
        }
        return out;
    }

    public static byte[] encryptBytes(byte[] payloadUtf8, String timeKey) {
        int[] t = parseKaalkaTimeKey(timeKey);
        return proc(payloadUtf8, true, t[0], t[1], t[2]);
    }

    public static byte[] decryptBytes(byte[] ciphertext, String timeKey) {
        int[] t = parseKaalkaTimeKey(timeKey);
        return proc(ciphertext, false, t[0], t[1], t[2]);
    }
}
