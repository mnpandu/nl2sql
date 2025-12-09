import javax.persistence.Query;
import java.lang.reflect.Field;
import java.math.BigDecimal;
import java.util.*;

public class SmartNativeQueryMapper {

    public static <T> List<T> mapToVO(Query query, Class<T> clazz) {
        // Get column names from result metadata
        List<String> columnNames = extractColumnNames(query);

        // Execute query
        List<Object[]> rows = query.getResultList();

        // Build column index map
        Map<String, Integer> indexMap = buildIndexMap(columnNames);

        return convertRows(rows, indexMap, clazz);
    }

    // Extracts column names from SQL query using Hibernate metadata
    private static List<String> extractColumnNames(Query query) {
        org.hibernate.query.NativeQuery nativeQuery =
                query.unwrap(org.hibernate.query.NativeQuery.class);

        List<String> columnNames = new ArrayList<>();
        for (org.hibernate.query.NativeQuery.ReturnableReturn returnable
                : nativeQuery.getReturnTypes()) {
            columnNames.add(returnable.getName().toLowerCase());
        }
        return columnNames;
    }

    private static Map<String, Integer> buildIndexMap(List<String> columnNames) {
        Map<String, Integer> map = new HashMap<>();
        for (int i = 0; i < columnNames.size(); i++) {
            map.put(columnNames.get(i).toLowerCase(), i);
        }
        return map;
    }

    private static <T> List<T> convertRows(List<Object[]> rows,
                                           Map<String, Integer> indexMap,
                                           Class<T> clazz) {

        List<T> result = new ArrayList<>();

        for (Object[] row : rows) {
            try {
                T obj = clazz.getDeclaredConstructor().newInstance();

                for (Field field : clazz.getDeclaredFields()) {
                    field.setAccessible(true);

                    String fieldName = field.getName().toLowerCase();

                    if (!indexMap.containsKey(fieldName)) continue;

                    int idx = indexMap.get(fieldName);
                    Object val = row[idx];

                    if (val != null) {
                        field.set(obj, convert(val, field.getType()));
                    }
                }

                result.add(obj);

            } catch (Exception e) {
                throw new RuntimeException("Failed mapping row", e);
            }
        }

        return result;
    }

    private static Object convert(Object val, Class<?> targetType) {

        if (val == null) return null;

        if (targetType.equals(Long.class))
            return ((Number) val).longValue();

        if (targetType.equals(Integer.class))
            return ((Number) val).intValue();

        if (targetType.equals(Double.class))
            return Double.valueOf(val.toString());

        if (targetType.equals(String.class))
            return val.toString();

        return val;
    }
}
