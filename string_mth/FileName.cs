using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace string_mth
{
    internal class Mth_obr
    {

        public static string resolve(string str)
        {
            // 2 + 3 - 6
            List<int> list_numbers = new List<int>();
            List<char> list_signs = new List<char>() { '+'};


            string prio_new_str = "";
            bool skob_trig = false;
            // signs first
            for (int i = 0; i < str.Length; i++)
            {
                
                if (str[i] == '(') { skob_trig = true; }

                else if (str[i] == ')') { skob_trig = false; }

                if (skob_trig) prio_new_str += str[i];
            }

            bool num_trig = false;
            string need = "";
            for (int i = 0; i < str.Length; i++)
            {
                
                int n;
                if (int.TryParse(Convert.ToString(str[i]), out n))
                {
                    num_trig = true;
                }
                else
                {
                    if (Convert.ToString(str[i]) == " ")
                    {
                        if (need != "") { list_numbers.Add(Convert.ToInt32(need)); }
                        need = "";
                        num_trig = false;
                    }
                    else
                    {
                        list_signs.Add(str[i]);
                    }
                }

                if (num_trig)
                {
                    need += str[i];
                }
            }
            list_numbers.Add(Convert.ToInt32(need));

            int now = 0;

            // "+ 5 * 2 - 10 / 2 + 30"

            for (int i = 0; i < list_signs.Count; i++)
            {
                if (list_signs[i] == '/')
                {
                    list_numbers[i] = list_numbers[i - 1] / list_numbers[i];
                    list_numbers.RemoveAt(i - 1);
                    list_signs.RemoveAt(i);
                }
            }

            for (int i = 0; i < list_signs.Count; i++)
            {
                if (list_signs[i] == '*')
                {
                    list_numbers[i] = list_numbers[i] * list_numbers[i - 1];
                    list_numbers.RemoveAt(i - 1);
                    list_signs.RemoveAt(i);
                }
            }

            for (int i = 0; i < list_numbers.Count; i++)
            {
                switch (list_signs[i])
                {
                    case '+':
                        now += list_numbers[i];
                        break;
                    case '-':
                        now -= list_numbers[i];
                        break;
                }
            }

            //list_numbers.ForEach(Console.WriteLine);
            //Console.WriteLine("--------------");
            //list_signs.ForEach(Console.WriteLine);

            return $"{now}";
        }

    }
}
