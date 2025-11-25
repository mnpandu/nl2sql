public class Employee {
    private int empId;
    private String empName;
    private double salary;
    private String address;

    public Employee(int empId, String empName, double salary, String address) {
        this.empId = empId;
        this.empName = empName;
        this.salary = salary;
        this.address = address;
    }

    public int getEmpId() { return empId; }
    public String getEmpName() { return empName; }
    public double getSalary() { return salary; }
    public String getAddress() { return address; }
}
