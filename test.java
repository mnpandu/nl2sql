import java.lang.reflect.Field;

public class MergeUtil {

    public static void merge(Object source, Object target) {
        Field[] sourceFields = source.getClass().getDeclaredFields();
        Field[] targetFields = target.getClass().getDeclaredFields();

        for (Field sField : sourceFields) {
            try {
                sField.setAccessible(true);
                Object value = sField.get(source);
                if (value == null) continue;

                // check if target has same field
                for (Field tField : targetFields) {
                    if (tField.getName().equals(sField.getName())) {
                        tField.setAccessible(true);
                        tField.set(target, value);
                    }
                }

            } catch (IllegalAccessException e) {
                throw new RuntimeException("Merge failed", e);
            }
        }
    }
}
