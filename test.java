import java.lang.reflect.Field;
import java.math.BigDecimal;
import java.util.*;

public class NativeQueryMapper {

    public static <T> List<T> map(Object[] columns, List<Object[]> rows, Class<T> clazz) {
        List<T> results = new ArrayList<>();

        Field[] fields = clazz.getDeclaredFields();
        Map<String, Field> fieldMap = new HashMap<>();

        // Build field-name → Field lookup table
        for (Field f : fields) {
            f.setAccessible(true);
            fieldMap.put(f.getName().toLowerCase(), f);
        }

        for (Object[] row : rows) {
            try {
                T instance = clazz.getDeclaredConstructor().newInstance();

                for (int i = 0; i < columns.length; i++) {

                    String colName = columns[i].toString().toLowerCase();  // from SQL alias
                    Object value = row[i];

                    if (value == null) continue;

                    if (fieldMap.containsKey(colName)) {
                        Field field = fieldMap.get(colName);

                        // Convert numeric types safely
                        Object casted = convertValue(value, field.getType());

                        field.set(instance, casted);
                    }
                }

                results.add(instance);
            } catch (Exception e) {
                throw new RuntimeException("Failed mapping for class " + clazz.getName(), e);
            }
        }
        return results;
    }

    private static Object convertValue(Object value, Class<?> targetType) {

        if (value == null) return null;

        if (targetType.equals(Long.class)) {
            return (value instanceof BigDecimal)
                    ? ((BigDecimal) value).longValue()
                    : Long.valueOf(value.toString());
        }

        if (targetType.equals(Integer.class)) {
            return (value instanceof BigDecimal)
                    ? ((BigDecimal) value).intValue()
                    : Integer.valueOf(value.toString());
        }

        if (targetType.equals(Double.class)) {
            return Double.valueOf(value.toString());
        }

        return value.toString(); // default String
    }
}
