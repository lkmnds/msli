grammar MSL;

options {
    language=Python3;
}

digit = "0"|"1"|"2"|"3"|"4"|"5"|"6"|"7"|"8"|"9"
sign   = "+" | "-"
number = [sign] {digit}

factor     = number | "(" expression ")"
component  = factor [{("*" | "/") factor}]
expression = component [{("+" | "-") component}]
