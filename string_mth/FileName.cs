using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace string_mth
{
    internal class Mth_obr
    {

        private static string solve(string str)
        {
            List<double> list_numbers = new List<double>();
            List<char> list_signs = new List<char>() { '+' };


            string need = "";
            str = str.Replace(" ", "");
            for (int i = 0; i < str.Length; i++)
            {
                if (int.TryParse(Convert.ToString(str[i]), out var n))
                {
                    need += str[i];
                }
                else
                {
                    list_signs.Add(str[i]);
                    list_numbers.Add(Convert.ToDouble(need));
                    need = "";
                }
            }
            list_numbers.Add(Convert.ToInt32(need));


            for (int i = 0; i < list_signs.Count; i++)
            {
                if (list_signs[i] == '/')
                {
                    list_numbers[i] = Convert.ToDouble(list_numbers[i - 1]) / Convert.ToDouble(list_numbers[i]);
                    list_numbers.RemoveAt(i - 1);
                    list_signs.RemoveAt(i);
                }
            }

            for (int i = 0; i < list_signs.Count; i++)
            {
                if (list_signs[i] == '*')
                {
                    list_numbers[i] = Convert.ToDouble(list_numbers[i - 1]) * Convert.ToDouble(list_numbers[i]);
                    list_numbers.RemoveAt(i - 1);
                    list_signs.RemoveAt(i);
                }
            }

            double now = 0;
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

            return $"{now}";
        }

        public static string resolve(string str)
        {
            while (str.Contains("sqrt("))
            {
                int ind = str.IndexOf("sqrt(");
                int ind1 = str.IndexOf(")");
                string num = str.Substring(ind + 5, ind1 - 1 - (ind + 5) + 1);
                str = str.Remove(ind, ind1 - ind + 1);
                str = str.Insert(ind, Convert.ToString(Math.Sqrt(Convert.ToDouble(num))));
            }

            string prio_new_str = "";
            string prio_new_str1 = "";
            bool skob_trig = false;
            for (int i = 0; i < str.Length; i++)
            {
                try
                {
                    if (str[i] == '(') { skob_trig = true; i++; }

                    else if (str[i] == ')') { skob_trig = false; prio_new_str1 += solve(prio_new_str); prio_new_str = ""; i++; }

                    if (skob_trig) prio_new_str += str[i];

                    else prio_new_str1 += str[i];
                }
                catch { }
            }
            return solve(prio_new_str1);
        }

    }
}
