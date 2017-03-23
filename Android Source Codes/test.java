
public class test {
    public static void main(String[] args){
        String part1 = "FFC07F80FF01FE03FFFFFFF3FFE7FFCFFF9C7F38FE71FCE3F87FF0FFE1FFC3FF87FF0E0E1C1F";
        String part2 = "00000100001C80000000001C0000080000060001C00000080000";
        char[][] array1 = new char[20][15];
        char[][] array2 = new char[20][15];
        StringBuilder binary1 = new StringBuilder();
        for (char c : part1.toCharArray()){
            int i = Integer.parseInt(String.valueOf(c), 16);
            String value = Integer.toBinaryString(i);
            int num_pad = 4 - value.length();
            String padding = "0000";
            String subStr = padding.substring(0, num_pad);
            binary1.append(subStr);
            binary1.append(value);
        }
        binary1.deleteCharAt(303);
        binary1.deleteCharAt(302);
        binary1.deleteCharAt(0);
        binary1.deleteCharAt(0);

        int explored = 0;
        for (int i = 0; i < 20; i++){
            for (int j = 0; j < 15; j++){
                char c = binary1.charAt(i * 15 + j);
                if (c == '1') explored++;
                array1[i][j] = c;
            }
        }

        StringBuilder binary2 = new StringBuilder();
        for (char c : part2.toCharArray()){
            int i = Integer.parseInt(String.valueOf(c), 16);
            String value = Integer.toBinaryString(i);
            int num_pad = 4 - value.length();
            String padding = "0000";
            String subStr = padding.substring(0, num_pad);
            binary2.append(subStr);
            binary2.append(value);
        }
        // remove padding
        binary2.delete(explored, binary2.length());
        int counter = 0;
        for (int i = 0; i < 20; i++){
            for (int j = 0; j < 15; j++){
                if (array1[i][j] == '1'){
                    array2[i][j] = binary2.charAt(counter);
                    counter++;
                }
                else {
                    array2[i][j] = '2';
                }
            }
        }


        char[][] result = new char[15][20];
        for (int i = 0; i < 15; i++){
            for (int j = 0; j < 20; j++){
                result[i][j] = array2[j][i];
            }
        }

        StringBuilder map_des = new StringBuilder();
        for (int i = 0; i < 15; i++){
            for (int j = 0; j < 20; j++){
                map_des.append(result[i][j]);
            }
        }
        System.out.println(map_des);
    }
}
